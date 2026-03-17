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
        print("Sender thread started successfully.")
        '''
        2. in a while loop run the below
        3. check for sender_interval 
        4. check if there have been changes since the last update packet was sent, if there have been changes then send an update packet to the neighbours and print the packet to STDOUT and reset the changed_update_packet flag to False
        '''

        self.node.connect_to_neighbours()
        while True:
            time.sleep(self.SENDER_INTERVAL)
            if self.changed_update_packet:
                self.send_to_neighbours()
                self.send_to_STDOUT()
                self.changed_update_packet = False

    def send_to_STDOUT(self):
        '''
        - Keep formatting of the update exactly the same as the update packet and what the listener receives
        '''
        pass

    def send_to_neighbours(self):
        pass