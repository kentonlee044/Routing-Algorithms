from threads import listener, routing_calculations, sender
import node
import threading
import sys
import time

def main():

    '''
    1. Read CLI arguments
    2. create node object (so the threads share the memory of the sockets)
    3. Create listener, sender, routing threads

    Input format - ./Routing.sh <Node-ID> <Port-Number> <Config-File> <Routing-Delay> <UpdateInterval>
    '''

    # Read CLI arguments
    if len(sys.argv) != 6:
        print("Error: Insufficient arguments provided. Usage: ./Routing.sh <Node-ID> <Port-NO> <Node-Config-File>")
        sys.exit(1)

    node_id, Port_NO, config_file, routing_delay, update_interval = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])

    # Check valid Node-ID
    if len(node_id) != 1 or not node_id.isalpha() or not node_id.isupper():
        print("Error: Invalid Node-ID")
        sys.exit(1)

    # Check valid port number
    try:
        Port_NO = int(Port_NO)
        if Port_NO < 6000:
            raise ValueError
        
    except ValueError:
        print("Error: Invalid Port number. Must be an integer.")
        sys.exit(1)
    

    # Assign constants to respective classes
    if routing_delay <= 0 or update_interval <= 0:
        raise ValueError("Routing delay and/or update interval must be positive integers.")
    
    routing_calculations.routing_calculations.ROUTING_DELAY = routing_delay
    sender.sender.SENDER_INTERVAL = update_interval

    try:
        print("")
        # Create node object
        node_obj = node.node(node_id, Port_NO, config_file)
        node_obj.parse_config_file(config_file)
        # Create server socket for the node
        node_obj.create_socket()

        # Create threads
        listener_thread = listener.listener(node_obj)
        routing_thread = routing_calculations.routing_calculations(node_obj)
        sender_thread = sender.sender(node_obj)
        print("")

    except Exception as e:
        
        print(f"Error: {e}")
        sys.exit(1)

    # Start threads
    listener_thread.start()
    routing_thread.start()
    sender_thread.start()

    try:
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Exiting program...")
        sys.exit(0)

if __name__ == "__main__":
    main()