import threading

class routing_calculations(threading.Thread):
    
    ROUTING_DELAY: int = None

    def __init__(self, node):
        super().__init__()
        self.node = node

    '''
    1. figure out how to receive the update packets from the listener thread, maybe we can use a queue to receive the packets from the listener thread?
    2. in a while loop run the below
    3. check for routing_delay
    4. if there are any update packets received from the listener thread then call dijkstra() to update the routing table and then call print_routing_table() to print the routing table to STDOUT
    '''
    def run(self):
        print("Routing thread started successfully.")

    '''
    Takes some the graph from a node?
    '''
    def dijkstra():
        pass

    def print_routing_table(self):
        pass

    def get_path(self, destination: str):
        pass