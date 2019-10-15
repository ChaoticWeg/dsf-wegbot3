from lib.wegbot import Wegbot
from .meta_admin_channel import MetaAdminChannelCog
from .meta_key_value import MetaKeyValueCog
from .meta_roles import MetaRolesCog


def setup(bot: Wegbot):
    bot.add_cog(MetaRolesCog(bot))
    bot.add_cog(MetaKeyValueCog(bot))
    bot.add_cog(MetaAdminChannelCog(bot))
