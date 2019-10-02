from discord.ext import commands


class DatabaseHandlingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot: commands.Bot = bot
        self.db = bot.get_cog("Database")

    def cog_check(self, ctx):
        return self.db is not None
