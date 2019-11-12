import discord
from discord.ext import commands

from lib.cogs.base import WegbotCog
from lib.wegbot import Wegbot


class VerifyCog(WegbotCog):
    """ Command for verifying users. Mods only. """

    @commands.guild_only()
    @WegbotCog.is_mod()
    @commands.command("verify")
    async def verify(self, ctx: commands.Context, member: discord.Member):
        role: discord.Role = discord.utils.get(ctx.guild.roles, name="Verified")

        if role is None:
            await ctx.send(f"{ctx.author.mention}, i tried to find a role called `Verified` but couldn't find one.")
            return

        await member.add_roles(role, reason=f"Verified by {ctx.author} via ?verify")

        msg: str = f"{member.mention}, you have been verified by {ctx.author.mention}!"
        welcome_channel: discord.TextChannel = discord.utils.get(ctx.guild.channels, name="welcome")
        if welcome_channel is not None and isinstance(welcome_channel, discord.TextChannel):
            msg = msg + f"\nSee {welcome_channel.mention} for rules and roles."

        await ctx.send(msg)


def setup(bot: Wegbot):
    bot.add_cog(VerifyCog(bot))
