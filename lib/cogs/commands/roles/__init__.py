from .roles import RolesCog
from lib.wegbot import Wegbot


def setup(bot: Wegbot):
    bot.add_cog(RolesCog(bot))
