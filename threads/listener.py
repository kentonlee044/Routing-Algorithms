import threading
import node

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
        print("Listener thread started successfully.")
        # TODO - call node's accept_neighbours() function to accept incoming connections from neighbours and test it

    '''
    sends the formatted command to the routing thread
    '''
    def handle_update(self):
        pass

    '''
    Parses the command from STDIN into a ready and usable format
    '''
    def read_command(self):
        pass