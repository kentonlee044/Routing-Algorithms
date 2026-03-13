import threading

class routing_calculations(threading.Thread):
    
    ROUTING_DELAY: int = None

    def __init__(self, node):
        super().__init__()
        self.node = node

    def run(self):
        print("Routing thread started successfully.")

    '''
    Takes some the graph from a node?
    '''
    def dijkstra():
        pass