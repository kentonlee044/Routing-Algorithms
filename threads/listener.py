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

    '''
    Thread should be running over this function listening for input and calling handle_update() before calling forward_update() to send the update packets to the routing calculations thread
    - Needs to call node's function to listen for updates from the neighbours and update the graph accordingly
    - also needs to call node's functions to 
    - needs to call accept_neighbours()
    '''
    def run(self):
        
        self.node.server_socket.settimeout(1) 
        # self.node.accept_connections()
        self.node.connections_ready.wait()  # Wait until connections are ready

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
                # message here is the socket object
                else:
                    try:
                        
                        data = message.recv(1024).decode().strip()
                        if data:
                            print(f"DEBUG: Received data from neighbour socket {message.getsockname()}: {data}")
                            self.handle_packet(data, message)
                            
                        else:
                            print("ERROR: Neighbour socket closed.")
                            time.sleep(5)
                    except Exception as e:
                        print(f"Error receiving from neighbour socket: {e}")
                        time.sleep(3)

    '''
    Takes in the command from STDIN and compares the command to the expected command and computes expected outcome
    '''
    def handle_stdin(self, data: str) -> None:
        # TODO need to find how to implement with QUERY PATH and BATCH UPDATE commands as they have two words in the command type but we can just split the command and then check the first word to determine the command type and then check the second word if needed for QUERY PATH and BATCH UPDATE
        
        separated_data = data.split(" ", 1)
        command = separated_data[0]
        if len(separated_data) < 2:
            print(f"Invalid command: {data}")
            os._exit(1)

        args = separated_data[1]

        get_command = command_types.get(command)
        if get_command:
            old_graph = copy.deepcopy(self.node.graph)
            get_command(self.node).execute(args)
            self.node.queue.put((command, args))    # Signal routing thread
            
            with self.node.update_lock:
                if self.node.graph != old_graph:
                    # If there are changes signal the sender thread to send an update packet to the neighbours
                    self.node.has_new_update = True
    
        else:
            # TODO need to setup error handling for each command type
            print(f"Invalid command: {command}")
            os._exit(1)

    '''
    Handle update packets from other nodes by reading data and updating the graph accordingly. A sending thread only sends packets to their direct neighbours so no need to continue forwarding this
    '''
    def handle_packet(self, packet: str, sender_socket) -> None:
        # TODO add error handling
        line = packet.strip()
        print(f"Received packet: {line}")

        if not line: 
            print(f"Error: Empty packet received.")
            os._exit(1)

        separated_data = line.split(" ", 1)
        command = separated_data[0]
        args = separated_data[1] 

        if command != "UPDATE":
            print(f"Error: Invalid update packet format.")
            return
        old_graph = copy.deepcopy(self.node.graph)
        UpdateCommand(self.node).execute(args)

        with self.node.update_lock:
            if self.node.graph != old_graph:
                self.node.has_new_update = True
                