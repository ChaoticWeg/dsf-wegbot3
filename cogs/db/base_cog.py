from discord.ext import commands
from .main_cog import DatabaseCog


class DatabaseHandlingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot: commands.Bot = bot
        self.db: DatabaseCog = bot.get_cog("Database")

    def cog_check(self, ctx):
        return self.db is not None
