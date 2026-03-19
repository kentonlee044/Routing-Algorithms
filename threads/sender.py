import threading
import time

class sender(threading.Thread):

    SENDER_INTERVAL: int = 1
    changed_update_packet: bool = False

    def __init__(self, node):
        super().__init__()
        self.node = node

    '''
    Calls self.node.connect_to_neighbours() to connect to the neighbours
    '''
    def run(self):
        '''
        2. in a while loop run the below
        3. check for sender_interval 
        4. check if there have been changes since the last update packet was sent, if there have been changes then send an update packet to the neighbours and print the packet to STDOUT and reset the changed_update_packet flag to False
        '''

        self.node.connect_to_neighbours()

        while True:
            time.sleep(self.SENDER_INTERVAL)
            with self.node.update_lock:
                if self.node.has_new_update and self.node.last_update_command:
                    self.relay(self.node.last_update_command)
                    self.node.has_new_update = False

    '''
    Relays an update packet to the neighbours through sockets and through STDOUT
    '''
    def relay(self, message: str) -> None:
        
        # Pass on the update packet with the source node's neighbours
        source_neighbours = ",".join(
            [f"{neighbour_id}:{info['cost']}:{info['port']}" for neighbour_id, info in self.node.neighbours.items()]
        )
        extra_update = f"UPDATE {self.node.node_ID} {source_neighbours}"
        full_message = f"{message}\n{extra_update}"

        for neighbour_id, sock in self.node.neighbour_sockets.items():
            # Don't send the update packet back to the sender
            if sock == self.node.last_update_sender:
                continue

            # Output to STDOUT
            print(message)
            
            # Output to neighbour sockets
            try:
                sock.sendall(full_message.encode())

            except Exception as e:
                print(f"Error sending update packet to neighbour {neighbour_id}: {e}")
        
