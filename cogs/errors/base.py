from discord.ext.commands import CommandError


class WegbotCommandError(CommandError):
    def __init__(self, message):
        super().__init__(message)
