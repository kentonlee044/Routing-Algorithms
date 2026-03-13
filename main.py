from threads import listener, routing_calculations, sender
import node
import threading
import sys

def main():

    '''
    1. Read CLI arguments
    2. create node object (so the threads share the memory of the sockets)
    3. Create listener, sender, routing threads

    Input format - ./Routing.sh <Node-ID> <Port-Number> <Config-File> <Routing-Delay> <UpdateInterval>
    '''

    # Read CLI arguments
    if len(sys.argv) != 6:
        print("Use format: ./Routing.sh <Node-ID> <Port-Number> <Config-File> <Routing-Delay> <UpdateInterval>")
        sys.exit(1)

    node_id, Port_NO, config_file, routing_delay, update_interval = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    
    # TODO: figure out how to assign ports

    # Assign constants to respective classes
    routing_calculations.routing_calculations.ROUTING_DELAY = routing_delay
    sender.sender.SENDER_INTERVAL = update_interval

    try:
        print("")
        # Create node object
        node_obj = node.node(node_id, Port_NO, config_file)
        print("Node object created successfully.")

        # Create threads
        listener_thread = listener.listener(node_obj)
        print("Listener thread created successfully.")
        routing_thread = routing_calculations.routing_calculations(node_obj)
        print("Routing thread created successfully.")
        sender_thread = sender.sender(node_obj)
        print("Sender thread created successfully.")
        print("")
    
    except Exception as e:
        
        print(f"Error creating node or thread object: {e}")
        sys.exit(1)

    # Start threads
    print("Starting threads...\n")
    listener_thread.start()
    routing_thread.start()
    sender_thread.start()

    # Wait for threads to finish 
    listener_thread.join()
    routing_thread.join()
    sender_thread.join()

if __name__ == "__main__":
    main()