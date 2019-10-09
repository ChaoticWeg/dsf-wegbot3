from discord.ext import commands
from lib.cogs.base import WegbotCog
from lib.errors.commands import CommandNotImplementedError


class MetaModsCog(WegbotCog, name="MetaMods"):
    """ Tools to determine which roles are mods """

    # @WegbotCog.has_table("mods")
    @commands.is_owner()
    @commands.group("mods")
    def cmd(self, ctx: commands.Context):
        raise CommandNotImplementedError(ctx.command)
