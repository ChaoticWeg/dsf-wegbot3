from .meta_roles import MetaRolesCog
from .meta_key_value import MetaKeyValueCog
from lib.wegbot import Wegbot


def setup(bot: Wegbot):
    bot.add_cog(MetaRolesCog(bot))
    bot.add_cog(MetaKeyValueCog(bot))
