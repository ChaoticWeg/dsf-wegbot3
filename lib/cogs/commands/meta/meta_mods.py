import discord
from discord.ext import commands

from lib.cogs.base import WegbotCog


class MetaModsCog(WegbotCog, name="MetaMods"):
    """ Tools to determine which roles are mods """

    @WegbotCog.has_table("mods")
    @WegbotCog.is_mod()
    @commands.guild_only()
    @commands.group("mods")
    async def cmd(self, ctx: commands.Context):
        """ List mods """
        if ctx.invoked_subcommand is None:
            await self.list.invoke(ctx)

    @cmd.command("list")
    async def list(self, ctx: commands.Context):
        """ List mods """
        mod_ids = self.db.mods.get_all(ctx.guild)
        msg = f"there are {'no' if len(mod_ids) == 0 else len(mod_ids)} mods in this server" if not len(mod_ids) == 1 \
            else "there is 1 mod in this server"
        await ctx.send(f"{ctx.author.mention}, {msg}. due to API restrictions, i can't list mods at the moment.")

    @cmd.command("check")
    async def check(self, ctx: commands.Context, member: discord.Member):
        """ Check whether a user is a mod """
        is_mod = self.db.mods.is_mod(member)
        is_mod_str = "is" if is_mod else "is not"
        await ctx.send(f"{ctx.author.mention}, `{member}` {is_mod_str} a mod.")

    @cmd.command("add")
    async def add(self, ctx: commands.Context, member: discord.Member):
        """ Add a mod by mentioning them """
        if self.db.mods.is_mod(member):
            await ctx.send(f"{ctx.author.mention}, `{member}` is already a mod.")
            return

        if member.bot:
            await ctx.send(f"{ctx.author.mention}, `{member}` is a bot and cannot be a mod.")
            return

        self.db.mods.add(member)
        await ctx.send(f"{ctx.author.mention}, i have added `{member}` as a mod.")

    @cmd.command("remove")
    async def remove(self, ctx: commands.Context, member: discord.Member):
        """ Remove a mod by mentioning them """
        if not self.db.mods.is_mod(member):
            await ctx.send(f"{ctx.author.mention}, `{member}` is not a mod.")
            return

        self.db.mods.remove(member)
        await ctx.send(f"{ctx.author.mention}, i have removed `{member}` as a mod.")
