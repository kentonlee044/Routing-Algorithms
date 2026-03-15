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
        '''
        1. First call node's connect_to_neighbours() function to connect to neighbours and test it (This should loop until all neighbours have been connected to meaning that we won't need to connect to neighbours again after this)
        2. in a while loop run the below
        3. check for sender_interval 
        4. check if there have been changes since the last update packet was sent, if there have been changes then send an update packet to the neighbours and print the packet to STDOUT and reset the changed_update_packet flag to False
        '''
        # TODO - call node's connect_to_neighbours() function to connect to neighbours and test it

    def send_to_STDOUT(self):
        pass

    def send_to_neighbours(self):
        pass