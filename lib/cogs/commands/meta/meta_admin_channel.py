import discord
from discord.ext import commands

from lib.cogs.base import WegbotCog


class MetaAdminChannelCog(WegbotCog, name="MetaAdminChannel", command_attrs=dict(hidden=True)):
    """ Get and set admin channel per guild """

    @commands.is_owner()
    @commands.guild_only()
    @WegbotCog.has_table("admin_channel")
    @commands.group("ac", aliases=["adminchannel"])
    async def cmd(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.get.invoke(ctx)

    @cmd.command("set")
    async def set(self, ctx: commands.Context):
        await ctx.trigger_typing()
        channel: discord.TextChannel = ctx.channel
        self.db.admin_channel.set(channel)
        new_channel: discord.TextChannel = self.db.admin_channel.get(ctx.guild)
        if new_channel is None:
            await ctx.send(f"{ctx.author.mention}, the channel wasn't set properly")
            return
        await ctx.send(f"{ctx.author.mention}, {new_channel.mention} is now the admin channel for this server")

    @cmd.command("get")
    async def get(self, ctx: commands.Context):
        await ctx.trigger_typing()
        channel: discord.TextChannel = self.db.admin_channel.get(ctx.guild)
        if channel is None:
            await ctx.send(f"{ctx.author.mention}, there isn't an admin channel set for this server")
            return
        await ctx.send(f"{ctx.author.mention}, the admin channel for this server is {channel.mention}")

    @cmd.command("delete")
    async def delete(self, ctx: commands.Context):
        await ctx.trigger_typing()
        self.db.admin_channel.delete(ctx.guild)
        should_be_none = self.db.admin_channel.get(ctx.guild)
        if should_be_none is not None:
            await ctx.send(f"{ctx.author.mention}, i wasn't able to unlink the admin channel for this server")
            return
        await ctx.send(f"{ctx.author.mention}, i have unlinked the admin channel for this server")
