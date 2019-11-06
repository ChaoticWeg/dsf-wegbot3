from discord import Member
from discord.ext.commands import CheckFailure, Command


class WegbotCheckFailure(CheckFailure):
    pass


class InvalidTableError(WegbotCheckFailure):
    """ The command requires a table that does not exist """

    def __init__(self, command: Command, tablename: str):
        super().__init__(f"Command '{command.name}' requires table '{tablename}' that does not exist or is unreachable")
        self.command = command
        self.tablename = tablename


class MemberIsNotModError(WegbotCheckFailure):
    """ The command requires the member to be a mod, and they are not """

    def __init__(self, command: Command, member: Member):
        super().__init__(f"Command '{command.name}' requires the user to be a mod, and {member} is not a mod")
        self.command = command
        self.member = member
