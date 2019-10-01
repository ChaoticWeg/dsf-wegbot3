from discord.ext import commands

# expose DatabaseHandlingCog to other modules
from .base_cog import DatabaseHandlingCog

# expose DatabaseCog to other modules
from .main_cog import DatabaseCog


def setup(bot: commands.Bot):
    bot.add_cog(DatabaseCog(bot))
    bot.get_cog("Database").initialize()


def teardown(bot: commands.Bot):
    bot.get_cog("Database").close()
