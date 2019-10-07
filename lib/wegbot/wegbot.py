from discord.ext import commands

from ..database import WegbotDatabase


class Wegbot(commands.Bot):
    """ Wegbot - subclass of discord.ext.commands.Bot """

    description: str = "Wegbot - resident idiot role-lord"

    def __init__(self, command_prefix="?"):
        super().__init__(command_prefix, description=Wegbot.description)
        self.db: WegbotDatabase = WegbotDatabase()
