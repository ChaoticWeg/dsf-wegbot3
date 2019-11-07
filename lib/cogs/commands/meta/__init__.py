from lib.wegbot import Wegbot
from .meta_admin_channel import MetaAdminChannelCog
from .meta_key_value import MetaKeyValueCog
from .meta_permission_request import MetaPermissionRequestCog
from .meta_roles import MetaRolesCog
from .meta_mods import MetaModsCog


def setup(bot: Wegbot):
    bot.add_cog(MetaRolesCog(bot))
    bot.add_cog(MetaKeyValueCog(bot))
    bot.add_cog(MetaAdminChannelCog(bot))
    bot.add_cog(MetaModsCog(bot))
    bot.add_cog(MetaPermissionRequestCog(bot))
