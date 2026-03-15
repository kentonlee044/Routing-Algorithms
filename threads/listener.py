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
        # TODO - 1. call node's accept_neighbours() function to accept incoming connections from neighbours and test it (This should loop until all neighbours have been connected to meaning that we won't need to accept from neighbours again after this)
        # TODO - 2. start a while loop to listen for updates from neighbours and call handle_update() to update the graph and then call forward_update() to send the update packets to the routing calculations thread
        # TODO - 3. need to also listen for updates from STDIN and call handle_update() to update the graph and then call forward_update() to send the update packets to the routing calculations thread
        # TODO - 4. need to figure out how to do both 2 and 3 at the same time because calling one will block the other, maybe we can use select to listen for both at the same time? or maybe use the timeout parameter of the socket to periodically check for updates from STDIN?

        ## If i need to use the listener thread to forward update packets to the routing calculations thread do i need to get an instance of the sender thread or can i just create a method that sends the packets directly to the routing calculations thread but this might go against the idea of 'listener' thread. Or what other options do i have for sending the update packets to the routing calculations thread? Maybe we can use a queue to send the packets from the listener thread to the routing calculations thread?
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