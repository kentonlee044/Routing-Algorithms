from typing import List, Dict

class node:
    
    '''
    - self.socket: The socket object that the other nodes will use to contact this node
    - self.neightbour_sockets: Will hold the neighbours ID and port numeber of the socket that the node will use to contact the neighbour
    - self.graph: This will be the graph that the node uses for routing calculations, represents what this node knows so far about the network so far. First string representing the source node, inside the dictionary represents the edges the source node has and its costs. This graph is used to update the routing table
    - self.routing_table: Table that represents the shortest path to each node. First string representing the destination node, the second string representing the next hop and the int representing the cost to get to the destination through that next hop
    '''
    def __init__(self, node_ID: str, Port_NO: int, config_file: str):
        self.node_ID = node_ID
        self.Port_NO = Port_NO
        self.config_file = config_file
        self.neighbours: Dict[str, Dict[int, int]] = {}
        self.socket = None  
        self.neighbour_sockets: Dict[str, any] = {}  
        self.graph: Dict[str, Dict[str, int]] = {}  
        self.routing_table: Dict[str, Dict[str, int]] = {}  

    def parse_config_file():
        pass

    def create_neighbour_list():
        pass

    def create_socket():
        pass

    def connect_to_neighbours():
        pass