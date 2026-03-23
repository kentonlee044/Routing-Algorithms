from typing import List, Dict
import time
import socket
import queue
import sys, os
import threading

class node: 
    
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
        self.queue = queue.Queue()  # thread safe queue for communication between threads
        self.has_new_update: bool = False
        self.update_lock = threading.Lock()
        self.neighbours: Dict[str, Dict[str, int]] = {}
        self.neighbour_sockets: Dict[str, any] = {}  
        self.graph: Dict[str, Dict[str, int]] = {}  
        self.routing_table: Dict[str, Dict] = {}  
        self.connections_ready = threading.Event()  
        self.failed_nodes = set()
        self.is_down = False
        self.initial_routing_printed = threading.Event()

    '''
    Parse the config file and populate self.neighbours with the neighbour ID as the key and a dictionary containing the cost and port number as the value. Also update self.num_neighbours to reflect the number of neighbours this node has.
    '''
    def parse_config_file(self, config_file: str) -> None:
        try:
            with open(config_file, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    try:
                        if len(line.strip()) == 1 and int(line):
                            self.num_neighbours = int(line)
                        
                        elif len(parts) == 3:
                            neighbour_id, cost, port = parts
                            
                            try:
                                if float(cost) <= 0:    
                                    raise ValueError
                                
                                self.neighbours[neighbour_id] = {'cost': float(cost), 'port': int(port)}

                                if self.node_ID in self.graph:
                                    self.graph[self.node_ID][neighbour_id] = float(cost)
                                else:
                                    self.graph[self.node_ID] = {neighbour_id: float(cost)}
                            except ValueError:
                                print(f"Error: Invalid configuration file format. (Each neighbour entry must have exactly three tokens; cost must be numeric.)")
                                os._exit(1)
                        else:
                            print(f"Error: Invalid configuration file format.")
                            os._exit(1)
                    except ValueError:
                        print(f"Error: Invalid configuration file format. (First line must be an integer.)")

        except FileNotFoundError:
            print(f"Error: Configuration file '{config_file}' not found.")
            os._exit(1)

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
                        
                    except Exception as e:
                        time.sleep(1)

    '''
    Accept incoming connections from neighbour nodes and add the socket to self.neighbour_sockets
    '''
    def accept_connections(self) -> None:
        
        threads = []
        connections_to_accept = len([n for n in self.neighbours if n < self.node_ID])  # Only accept connections from neighbours with smaller IDs
        while len(threads) < connections_to_accept:
            try:
                conn, addr = self.server_socket.accept()
                t = threading.Thread(target=self._assign_connection, args=(conn,))
                threads.append(t)
                t.start()
                
            except socket.timeout:
                continue

            except Exception as e:
                print(f"Error accepting connection: {e}")
                time.sleep(1)
        for t in threads:
            t.join()
    '''
    Create new thread for each connection so it doesn't block the accepting of other connections
    '''
    def _assign_connection(self, conn):
        try:
            node_id = conn.recv(1024).decode()
            if node_id and node_id not in self.neighbour_sockets:
                self.neighbour_sockets[node_id] = conn
            
        except Exception as e:
            print(f"Error assigning connection: {e}")

    '''
    address holds the neighbours (IP, port) and the socket is the socket object that the node will use to contact the neighbour. 
    '''

    def create_socket(self) -> None:
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('', self.Port_NO))
            self.server_socket.listen()
            # print(f"Socket created and listening on port {self.Port_NO}")

        except Exception as e:
            print(f"Error creating socket: {e}")

