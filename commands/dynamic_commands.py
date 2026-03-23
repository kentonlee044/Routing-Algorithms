from abc import ABC, abstractmethod
import os

# TODO add error handling for missing and extra tokens
class Command(ABC):

    def __init__(self, node):
        self.node = node

    @abstractmethod
    def execute(self, args: str) -> None:
        pass

class UpdateCommand(Command):

    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        
        separated_data = args.split(" ", 1)
        source_node = separated_data[0]
        params = separated_data[1] 
        
        self._update_neighbours(source_node, params)
        print(self.node.graph)
    
    '''
    Helper function of execute()
    '''
    def _update_neighbours(self, source_node: str, params: str) -> None:
        
        params_list = params.split(",")

        for param in params_list:
            neighbour_id, cost, _ = param.split(":")
            if source_node in self.node.graph:
                self.node.graph[source_node][neighbour_id] = float(cost)
            else:
                self.node.graph[source_node] = {neighbour_id: float(cost)}
            
            if neighbour_id in self.node.graph:
                self.node.graph[neighbour_id][source_node] = float(cost)
            else:
                self.node.graph[neighbour_id] = {source_node: float(cost)}

class ChangeCommand(Command):

    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        separated_data = args.split(" ")
        if len(separated_data) > 2:
                print("Error: Invalid command format. Expected exactly two tokens after CHANGE.")
                os._exit(1)
        try: 
            test_int = float(separated_data[1])  
            if len(separated_data) != 2:
                raise ValueError
        except ValueError:
            print("Error: Invalid command format. Expected numeric cost value.")
            os._exit(1)

        neighbour_id = separated_data[0]
        cost = float(separated_data[1]) 

        self.node.graph[self.node.node_ID][neighbour_id] = cost
        
        if neighbour_id in self.node.graph:
            self.node.graph[neighbour_id][self.node.node_ID] = cost


class FailCommand(Command):
    
    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        node_id = args.strip()

        if len(node_id) != 1 or not node_id.isalpha() or not node_id.isupper():
            print("Error: Invalid command format. Expected a valid Node-ID.")
            os._exit(1)

        if node_id == self.node.node_ID:
            self.node.is_down = True
            print(f"Node {node_id} is now DOWN.")
        else:
            self.node.failed_nodes.add(node_id)
            # Remove the failed node from the graph to reflect its failure
            if node_id in self.node.graph:
                del self.node.graph[node_id]
            
            # Remove the failed node from the neighbours of other nodes in the graph
            for source in self.node.graph:
                if node_id in self.node.graph[source]:
                    del self.node.graph[source][node_id]
                    print(self.node.graph)

class RecoverCommand(Command):

    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        node_id = args.strip()

        if len(node_id) != 1 or not node_id.isalpha() or not node_id.isupper():
            print("Error: Invalid command format. Expected a valid Node-ID.")
            os._exit(1)
        if node_id == self.node.node_ID:
            self.node.is_down = False
            print(f"Node {node_id} is now UP.")
        else:
            if node_id in self.node.failed_nodes:
                self.node.failed_nodes.discard(node_id)

class QueryCommand(Command):

    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        destination = args.strip()
        self._check_valid_args(destination)

        # if destination not in self.node.routing_table:
        #     print(f"No path from {self.node.node_ID} to {destination} found.")
        #     return
        
        data = self.node.routing_table[destination]
        print(f"Least cost path from {self.node.node_ID} to {destination}: {data['path']}, link cost: {data['cost']}")
    
    def _check_valid_args(self, args):
        if len(args) != 1 :
            print("Error: Invalid command format. Expected a valid Destination.")
            os._exit(1)

class QueryPathCommand(Command):

    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        self._check_valid_args(args.strip())
        source_node, destination_node = args.strip().split(" ")
        distances, previous = self.node.routing_thread.dijkstra(source_node)
        path = self._get_path(distances, previous, destination_node)
        print(f"Least cost path from {source_node} to {destination_node}: {path}, link cost: {distances[destination_node]}")

    def _check_valid_args(self, args):
        parts = args.split(" ")
        if len(parts) != 2:
            print("Error: Invalid command format. Expected two valid identifiers for Source and Destination.")
            os._exit(1)
        if not parts[0].isalpha() or not parts[0].isupper() or len(parts[0]) != 1:
            print("Error: Invalid command format. Expected valid Node-ID for Source.")
            os._exit(1)
        
        if not parts[1].isalpha() or not parts[1].isupper() or len(parts[1]) != 1:
            print("Error: Invalid command format. Expected valid Node-ID for Destination.")
            os._exit(1)

        # if parts[0] not in self.node.routing_table:
        #     print(f"No path from {parts[0]} to {parts[1]} found.")
        #     return

        # if parts[1] not in self.node.routing_table:
        #     print(f"No path from {parts[0]} to {parts[1]} found.")
        #     return
        
    def _get_path(self, distances, previous_nodes, destination):
        if distances[destination] == float('inf'):
            return None
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path.reverse()
        return "".join(path)

class ResetCommand(Command):

    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        print(f"Executing RESET command with arguments: {args}")
        # TODO implement logic for RESET command

class BatchUpdateCommand(Command):

    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        print(f"Executing BATCH UPDATE command with arguments: {args}")
        # TODO implement logic for BATCH UPDATE command
