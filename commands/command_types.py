from commands.dynamic_commands import UpdateCommand, ChangeCommand, FailCommand, RecoverCommand, QueryCommand, QueryPathCommand, ResetCommand, BatchUpdateCommand

command_types = {
    "UPDATE": UpdateCommand,
    "CHANGE": ChangeCommand,
    "FAIL": FailCommand,
    "RECOVER": RecoverCommand,
    "QUERY": QueryCommand,
    "QUERY PATH": QueryPathCommand,
    "RESET": ResetCommand,
    "BATCH UPDATE": BatchUpdateCommand
}