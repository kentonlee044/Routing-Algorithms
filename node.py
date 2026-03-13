from typing import List, Dict
import time
import error
import socket

class node: # TODO Add locks to shareddata structure to avoid race conditions
    
    '''
    - self.socket: The socket object that the other nodes will use to contact this node
    - self.neighbour_sockets: Will hold the neighbours ID and port number of the socket that the node will use to contact the neighbour
    - self.graph: This will be the graph that the node uses for routing calculations, represents what this node knows so far about the network so far. First string representing the source node, inside the dictionary represents the edges the source node has and its costs. This graph is used to update the routing table
    - self.routing_table: Table that represents the shortest path to each node. First string representing the destination node, the second string representing the next hop and the int representing the cost to get to the destination through that next hop
    '''

    def __init__(self, node_ID: str, Port_NO: int, config_file: str):
        self.node_ID = node_ID
        self.Port_NO = Port_NO
        self.config_file = config_file
        self.server_socket = None  
        self.firstCall = True
        self.num_neighbours: int = 0
        self.neighbours: Dict[str, Dict[str, int]] = {}
        self.neighbour_sockets: Dict[str, any] = {}  
        self.graph: Dict[str, Dict[str, int]] = {}  
        self.routing_table: Dict[str, Dict[str, int]] = {}  

    '''
    Parse the config file and populate self.neighbours with the neighbour ID as the key and a dictionary containing the cost and port number as the value. Also update self.num_neighbours to reflect the number of neighbours this node has.
    '''
    def parse_config_file(self, config_file: str) -> None:
        with open(config_file, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(line.strip()) == 1 and int(line):
                    self.num_neighbours = int(line)

                elif len(parts) == 3:
                    neighbour_id, cost, port = parts
                    if float(cost) <= 0:
                        raise error.InvalidConfigFileError(f"Cost must be a positive integer in config file: {line}")
                    elif int(port) < 6000:
                        raise error.InvalidConfigFileError(f"Port number must be greater than 6000 in config file: {line}")
                    
                    self.neighbours[neighbour_id] = {'cost': float(cost), 'port': int(port)}
                    
                else:
                    raise error.InvalidConfigFileError(f"Invalid line in config file: {line}")
        
        print("Neighbours")
        print(self.neighbours)
        print()

    '''
    Updates the nodes knowledge of the graph with the new information received from the neighbours. This will be used to update the routing table.
    '''
    def update_graph(self) -> None:
        pass

    ''' 
    Updates the routing table for the node
    '''
    def update_routing_table(self) -> None:
        pass

    '''
    Try to connect to neighbours from self.neighbours and add the socket to self.neighbour_sockets. On failure wait a bit and try again.
    '''
    def connect_to_neighbours(self) -> None:
        for neighbour_id, info in self.neighbours.items():
            if self.node_ID < neighbour_id:                                                 # maintain one socket between any two nodes 
                while neighbour_id not in self.neighbour_sockets:
                    try:
                        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # for development purposes, allows us to reuse the same port without waiting for it to be released
                        client_sock.connect(('localhost', info['port']))
                        client_sock.sendall(self.node_ID.encode())
                        self.neighbour_sockets[neighbour_id] = client_sock
                        print(f"Connected to neighbour {neighbour_id} at port {info['port']}")

                    except Exception as e:
                        print(f"Error connecting to neighbour {neighbour_id} at port {info['port']}: {e}")
                        print("Retrying in 3 seconds...")
                        time.sleep(3)

    '''
    Accept incoming connections from neighbour nodes and add the socket to self.neighbour_sockets
    '''
    def accept_connections(self) -> None:
        while len(self.neighbour_sockets) < self.num_neighbours:
            try:
                conn, addr = self.server_socket.accept()
                node_id = conn.recv(1024).decode()
                self.neighbour_sockets[node_id] = conn
                print(f"Connected to neighbour {node_id} at {addr}")

            except Exception as e:
                print(f"Error accepting connection: {e}")
                time.sleep(1)

    '''
    address holds the neighbours (IP, port) and the socket is the socket object that the node will use to contact the neighbour. 
    '''

    def create_socket(self) -> None:
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('', self.Port_NO))
            self.server_socket.listen()
            print(f"Socket created and listening on port {self.Port_NO}")

        except Exception as e:
            print(f"Error creating socket: {e}")

    def update_neighbours(self):
        pass
