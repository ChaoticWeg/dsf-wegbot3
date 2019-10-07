from .meta_roles import MetaRolesCog
from lib.wegbot import Wegbot


def setup(bot: Wegbot):
    bot.add_cog(MetaRolesCog(bot))
