from datetime import datetime

import discord
from discord.ext import commands

from lib.cogs.base import WegbotCog
from lib.errors.commands import NoSuchRoleError, RolesNotClearedError


class MetaRolesCog(WegbotCog, name="MetaRoles"):

    @commands.guild_only()
    @WegbotCog.has_table("roles")
    @commands.group("roles")
    async def cmd(self, ctx: commands.Context):
        """ List available roles """
        if ctx.invoked_subcommand is None:
            await self.list.invoke(ctx)

    @cmd.command("list")
    async def list(self, ctx: commands.Context):
        """ List available roles """
        roles = self.db.roles.get_all(ctx.guild)
        role_names = [f"`{r.name}`" for r in roles if r is not None]

        roles_summary: str = "\n".join(role_names) if len(role_names) > 0 else "**(none)**"

        embed: discord.Embed = discord.Embed(
            timestamp=datetime.now(),
            description=f"{roles_summary}\n\nUse `?addrole <role>` to request one."
        )

        embed.set_author(name=f"Requestable roles in {ctx.guild.name}", icon_url=ctx.guild.icon_url)
        embed.set_footer(text="Powered by discord.py", icon_url="https://projects.chaoticweg.cc/supereyes.png")
        await ctx.send(embed=embed)

    @commands.is_owner()
    @cmd.command("add", hidden=True)
    async def add(self, ctx: commands.Context, *, role_name: str):
        """ Add a requestable role to the database """
        role: discord.Role = discord.utils.get(ctx.guild.roles, name=role_name)

        if role is None:
            raise NoSuchRoleError(role_name)

        # TODO check that role is not a mod role (users should NOT be able to request mod roles)

        self.db.roles.put(role)
        await ctx.send(f"{ctx.author.mention}, `{role.name}` can now be requested here.")

    @commands.is_owner()
    @cmd.command("remove", hidden=True)
    async def remove(self, ctx: commands.Context, *, role_name: str):
        """ Remove a requestable role from the database """
        role: discord.Role = discord.utils.get(ctx.guild.roles, name=role_name)

        if role is None:
            raise NoSuchRoleError(role_name)

        self.db.roles.remove(role)
        await ctx.send(f"{ctx.author.mention}, `{role.name}` can now **no longer** be requested here.")

    @commands.is_owner()
    @cmd.command("clear", hidden=True)
    async def clear(self, ctx: commands.Context):
        """ Clear all requestable roles from the database """
        self.db.roles.clear(ctx.guild)

        roles_left: int = self.db.roles.count(ctx.guild)
        if not roles_left == 0:
            raise RolesNotClearedError(ctx.guild)

        await ctx.send(f"{ctx.author.mention}, i have cleared all requestable roles from this server.")
