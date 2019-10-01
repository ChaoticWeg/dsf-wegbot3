from discord.ext import commands
from .roles import MetaRolesCog
from .mods import MetaModsCog
from .kv import MetaKeyValueCog


def setup(bot: commands.Bot):
    bot.add_cog(MetaRolesCog(bot))
    bot.add_cog(MetaModsCog(bot))
    bot.add_cog(MetaKeyValueCog(bot))
