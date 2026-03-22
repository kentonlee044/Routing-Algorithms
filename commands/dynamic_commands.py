from abc import ABC, abstractmethod
'''
- Define command functions here and define the logic of what each function does
- Create dictionary of type CommandType.command: functionPointer
'''

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
        # print(f"After update: {self.node.graph}")
    
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

class ChangeCommand(Command):

    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        print(f"Executing CHANGE command with arguments: {args}")
        separated_data = args.split(" ", 1)
        source_node = separated_data[0]
        cost = separated_data[1] 

        self._update_neighbours(source_node, cost)
    
    def _update_neighbours(self, source_node: str, cost: str) -> None:
        if source_node in self.node.graph:
            for neighbour in self.node.graph[source_node]:
                self.node.graph[source_node][neighbour] = float(cost)
        else:
            print(f"Error: Node {source_node} not found in graph.")

class FailCommand(Command):
    
    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        print(f"Executing FAIL command with arguments: {args}")
        # TODO implement logic for FAIL command

class RecoverCommand(Command):

    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        print(f"Executing RECOVER command with arguments: {args}")
        # TODO implement logic for RECOVER command

class QueryCommand(Command):

    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        print(f"Executing QUERY command with arguments: {args}")
        # TODO implement logic for QUERY command

class QueryPathCommand(Command):

    def __init__(self, node):
        super().__init__(node)

    def execute(self, args: str) -> None:
        print(f"Executing QUERY PATH command with arguments: {args}")
        # TODO implement logic for QUERY PATH command

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
