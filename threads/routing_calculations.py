import threading

class routing_calculations(threading.Thread):
    
    ROUTING_DELAY: int = 1

    def __init__(self, node):
        super().__init__()
        self.node = node

    '''
    2. in a while loop run the below
    3. check for routing_delay
    4. if there are any update packets received from the listener thread then call dijkstra() to update the routing table and then call print_routing_table() to print the routing table to STDOUT
    '''
    def run(self):
        print("Routing thread started successfully.")

        while True:
            # Blocking call, waits for an event from the listener thread
            event, source_node, params = self.node.queue.get()  

            print(f"\nRouting thread received event: {event} from source node: {source_node} with params: {params}")
            if event == "UPDATE":
                self.dijkstra()
    '''
    takes self.graph and updates the routing table
    '''
    def dijkstra(self):
        pass

    def print_routing_table(self):
        pass

    def get_path(self, destination: str):
        pass