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
        accepting_thread = threading.Thread(target=self.node.accept_connections)
        accepting_thread.start()
        self.node.connect_to_neighbours()
        accepting_thread.join()
        self.node.connections_ready.set()  # Signal that connections are ready
        self.node.initial_routing_printed.wait()
        
        with self.node.update_lock:
            message = self.get_update_message()
            self.relay(message)

        while True:
            time.sleep(self.SENDER_INTERVAL)
            if self.node.is_down:
                continue

            with self.node.update_lock:
                if self.node.has_new_update:
                    message = self.get_update_message()
                    self.relay(message)
                    self.node.has_new_update = False

    '''
    Relays an update packet to the neighbours through sockets and through STDOUT
    '''
    def relay(self, message: str) -> None:
        
        # Output to STDOUT
        print(message)
        for neighbour_id, sock in self.node.neighbour_sockets.items():
            try:
                sock.sendall(message.encode())

            except Exception as e:
                print(f"Error sending update packet to neighbour {neighbour_id}: {e}")
        
        # self.node.last_update_sender = None
    
    
    def get_update_message(self) -> str:
        
        edges = self.node.graph.get(self.node.node_ID, {})
        source_neighbours = ",".join(
            f"{neighbour_id}:{cost}:{self.node.neighbours[neighbour_id]['port']}" for neighbour_id, cost in edges.items()
            if neighbour_id in self.node.neighbours
        )
        return f"UPDATE {self.node.node_ID} {source_neighbours}"
        
