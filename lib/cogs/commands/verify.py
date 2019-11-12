from discord import Member
from discord.ext import commands

from lib.cogs.base import WegbotCog


class VerifyCog(WegbotCog):
    """ Command for verifying users. Mods only. """

    @commands.guild_only()
    @WegbotCog.is_mod()
    @commands.command("verify")
    async def verify(self, ctx: commands.Context, member: Member):
        pass
