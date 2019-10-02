from discord.ext import commands
from ..errors import DatabaseNullError


class DatabaseHandlingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot: commands.Bot = bot
        self.db = bot.get_cog("Database")

    def cog_check(self, ctx):
        if self.db is None:
            raise DatabaseNullError(self.__class__.__name__)
