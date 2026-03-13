import threading

class sender(threading.Thread):

    SENDER_INTERVAL: int = None
    changed_update_packet: bool = False

    def __init__(self, node):
        super().__init__()
        self.node = node

    '''
    Calls self.node.connect_to_neighbours() to connect to the neighbours
    '''
    def run(self):
        print("Sender thread started successfully.")
        # TODO - call node's connect_to_neighbours() function to connect to neighbours and test it

    def send_to_STDOUT(self):
        pass

    def send_to_neighbours(self):
        pass