from discord.ext.commands import CheckFailure, Command


class WegbotCheckFailure(CheckFailure):
    pass


class InvalidTableError(WegbotCheckFailure):
    """ The command requires a table that does not exist """
    def __init__(self, command: Command, tablename: str):
        super().__init__(f"Command '{command.name}' requires table '{tablename}' that does not exist or is unreachable")
        self.command = command
        self.tablename = tablename
