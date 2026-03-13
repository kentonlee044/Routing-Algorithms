import threading

class sender(threading.Thread):

    SENDER_INTERVAL: int = None
    changed_update_packet: bool = False

    def __init__(self, node):
        super().__init__()
        self.node = node

    def run(self):
        print("Sender thread started successfully.")

    def send_to_STDOUT():
        pass

    def send_to_neighbours():
        pass