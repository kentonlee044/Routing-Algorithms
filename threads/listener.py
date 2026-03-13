import threading

class listener(threading.Thread):
    
    def __init__(self, node):
        super().__init__()
        self.node = node

    '''
    Thread should be running over this function listening for input and calling handle_update() before calling forward_update() to send the update packets to the routing calculations thread
    '''
    def run(self):
        print("Listener thread started successfully.")

    '''
    sends the formatted command to the routing thread
    '''
    def handle_update():
        pass

    '''
    Parses the command from STDIN into a ready and usable format
    '''
    def read_command():
        pass