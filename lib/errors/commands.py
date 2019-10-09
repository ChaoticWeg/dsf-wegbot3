from discord.ext.commands import Command, CommandError
from discord import Role, Guild


class WegbotCommandError(CommandError):
    """ Base command error """
    pass


class CommandNotImplementedError(WegbotCommandError):
    """ This command has not yet been implemented """
    def __init__(self, command: Command):
        super().__init__(f"command `{command.qualified_name}` has not yet been implemented. go shriek at weg about it.")


class NoSuchRoleError(WegbotCommandError):
    """ A user tried to perform a command involving a role that does not exist """
    def __init__(self, role_name):
        super().__init__(f"no such role: `{role_name}`")


class RoleNotRequestableError(WegbotCommandError):
    """ A user tried to request a role that cannot be requested """
    def __init__(self, role: Role):
        super().__init__(f"role `{role.name}` cannot be requested")


class RolesNotClearedError(WegbotCommandError):
    """ Owner tried to clear roles but they were not cleared for some reason """
    def __init__(self, guild: Guild):
        super().__init__(f"roles for **{guild.name}** were supposed to be cleared, but some are left")
