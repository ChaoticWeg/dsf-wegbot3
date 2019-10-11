from discord.ext import commands
from lib.database import WegbotDatabase

import discord


class Wegbot(commands.Bot):
    """ Wegbot - subclass of discord.ext.commands.Bot """

    description: str = "Wegbot - resident idiot role-lord"
    version: str = "v3.0.1"
    default_activity: discord.Activity = discord.Game(name=f"wegbot {version} – ?help")

    def __init__(self, command_prefix="?"):
        super().__init__(command_prefix, description=Wegbot.description, activity=Wegbot.default_activity)
        self.db: WegbotDatabase = WegbotDatabase()

    async def on_ready(self):
        print(f"logged in as {self.user}")
        self.db.initialize()
