import threading
import node
import select
import sys, os
import time
import copy
from commands.command_types import command_types
from commands.dynamic_commands import UpdateCommand, ChangeCommand, FailCommand, RecoverCommand, QueryCommand, QueryPathCommand, ResetCommand, BatchUpdateCommand

class listener(threading.Thread):
    
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.seen_packets = set()      

    def run(self):
        
        self.node.server_socket.settimeout(1) 
        self.node.connections_ready.wait()  

        while True:
            listen_list = list(self.node.neighbour_sockets.values())
            listen_list.append(sys.stdin)

            messages, _, _ = select.select(listen_list, [], [])

            for message in messages:
                if message == sys.stdin:
                    line = sys.stdin.readline().strip()
                    if line:
                        self.handle_stdin(line)
                
                # Receive messages from neighbour sockets
                else:
                    try:
                        
                        data = message.recv(1024).decode().strip()
                        if data:
                            self.handle_packet(data)
                            
                        else:
                            time.sleep(1)

                    except Exception as e:
                        time.sleep(1)

    '''
    Takes in the command from STDIN and compares the command to the expected command and computes expected outcome
    '''
    def handle_stdin(self, data: str) -> None:
        separated_data = data.split(" ", 1)
        command = separated_data[0]
        args = separated_data[1] if len(separated_data) > 1 else ""

        if args:
            if command in ["QUERY", "BATCH", "CYCLE"]:
                second_word = args.split(" ", 1)[0]
                if second_word in ["PATH", "UPDATE", "DETECT"]:
                    info = args.split(" ", 1)
                    command = command + " " + info[0]
                    args = info[1] if len(info) > 1 else ""
        
        get_command = command_types.get(command)
        if get_command:
            old_graph = copy.deepcopy(self.node.graph)
            get_command(self.node).execute(args)
            self.node.queue.put((command, args))            # Signal routing thread
            
            with self.node.update_lock:
                if self.node.graph != old_graph:
                    self.node.has_new_update = True         # If there are changes signal the sender thread to send an update packet to the neighbours
    
        else:
            print("Error: Invalid command.")
            os._exit(1)

    '''
    Handle update packets from other nodes by reading data and updating the graph accordingly. A sending thread only sends packets to their direct neighbours so no need to continue forwarding this
    '''
    def handle_packet(self, packet: str) -> None:
        line = packet.strip()

        if not line: 
            print(f"Error: Empty packet received.")
            os._exit(1)

        separated_data = line.split(" ", 1)
        command = separated_data[0]
        args = separated_data[1] 

        source_node = args.split(" ")[0]
        if source_node in self.node.failed_nodes:
            return

        if command != "UPDATE":
            print(f"Error: Invalid update packet format.")
            os._exit(1)

        if packet in self.seen_packets:
            return
        self.seen_packets.add(packet)

        old_source_edges = copy.deepcopy(self.node.graph.get(self.node.node_ID, {}))
        old_graph = copy.deepcopy(self.node.graph)
        UpdateCommand(self.node).execute(args)

        
        for neighbour_id, sock in self.node.neighbour_sockets.items():          # Forward the packet to neighbours except the source node
            if neighbour_id != source_node:
                try:
                    sock.sendall(packet.encode())
                except Exception as e:
                    print(f"Error forwarding packet to {neighbour_id}: {e}")

        with self.node.update_lock:
            new_source_edges = self.node.graph.get(self.node.node_ID, {})       # only compare for differences between the source node's graph since update packets only contain immediate neighbours
            if new_source_edges != old_source_edges:
                self.node.has_new_update = True
            if self.node.graph != old_graph:
                self.node.queue.put(("UPDATE", args))
                self.seen_packets = {packet}
                