import threading
import time
import copy

class routing_calculations(threading.Thread):
    
    ROUTING_DELAY: int = 1
    initial_compute: bool = False

    def __init__(self, node):
        super().__init__()
        self.node = node

    def run(self):
        # Initial computation and printing of the routing table based on the initial graph after delay
        time.sleep(self.ROUTING_DELAY)  
        self.dijkstra()  
        self.print_routing_table()
        
        while True:
            # Blocking call, waits for an event from the listener thread
            event = self.node.queue.get()  
            old_table = copy.deepcopy(self.node.routing_table)  
            self.dijkstra()

            # check for changes
            if self.node.routing_table != old_table:
                # print("changes found")
                self.print_routing_table()
                    
    '''
    Use self.node.graph to compute the shortest path from the source_node to every other node in self.node.graph
    '''
    def dijkstra(self):
        source_node = self.node.node_ID
        
        # Add all nodes to the set
        nodes = set(self.node.graph.keys())
        for neighbours in self.node.graph.values():
            nodes.update(neighbours.keys())

        # initialise distances and previous nodes
        distances = {node: float('inf') for node in nodes}
        distances[source_node] = 0
        previous_nodes = {node: None for node in nodes}
        visited = set()

        
        while len(visited) < len(distances):
            # sorts and selects the node by lowest cost
            current = min(
                (n for n in distances if n not in visited),
                key=lambda n: distances[n]
            )
            
            # closest node is unreachable
            if distances[current] == float('inf'):
                break

            visited.add(current)

            # Skip the inner keys
            if current not in self.node.graph:
                continue
            
            # Calculate new distances to neighbours
            for neighbour, cost in self.node.graph[current].items():
                new_distance = distances[current] + cost
                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    previous_nodes[neighbour] = current
        
        self.populate_routing_table(distances, previous_nodes)

    '''
    Helper function of dijkstra() 
    '''
    def populate_routing_table(self, distances: dict, previous_nodes: dict) -> None:
        source = self.node.node_ID
        self.node.routing_table = {}  # Clear existing routing table before populating new entries
        
        for destination in distances:
            
            # skip unreachable nodes
            if destination == source or distances[destination] == float('inf'):
                continue
            
            # Generate path from source to destination
            path = []
            current = destination
            while current is not None:
                path.append(current)
                current = previous_nodes[current]
            path.reverse()
            
            # Fill routing table entry
            next_hop = path[1]
            full_path = ''.join(path)
            self.node.routing_table[destination] = {
                'cost': distances[destination],
                'path': full_path,
                'next_hop': next_hop
            }

    def print_routing_table(self):
        print(f"I am Node {self.node.node_ID}", flush=True)
        for destination, data in sorted(self.node.routing_table.items()):
            print(f"Least cost path from {self.node.node_ID} to {destination}: {data['path']}, link cost: {data['cost']}", flush=True)