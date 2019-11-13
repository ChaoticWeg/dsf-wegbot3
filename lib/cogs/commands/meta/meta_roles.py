from datetime import datetime
import typing

import discord
from discord.ext import commands

from lib.cogs.base import WegbotCog
from lib.errors.commands import NoSuchRoleError, RolesNotClearedError


class MetaRolesCog(WegbotCog, name="MetaRoles"):
    """ Tools for determining which roles are requestable """

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
        roles: typing.List[discord.Role] = self.db.roles.get_all(ctx.guild)
        role_names: typing.List[str] = [f"`{r.name}`" for r in roles if r is not None] if roles is not None else []

        roles_summary: str = "\n".join(role_names) if len(role_names) > 0 else "**(none)**"

        embed: discord.Embed = discord.Embed(
            timestamp=datetime.now(),
            description=f"{roles_summary}\n\nUse `?addrole <role>` to request one."
        )

        embed.set_author(name=f"Requestable roles in {ctx.guild.name}", icon_url=ctx.guild.icon_url)
        embed.set_footer(text="Powered by discord.py", icon_url="https://projects.chaoticweg.cc/supereyes.png")
        await ctx.send(embed=embed)

    @WegbotCog.is_mod()
    @cmd.command("add", hidden=True)
    async def add(self, ctx: commands.Context, *role_names):
        """ Add a requestable role to the database """

        if len(role_names) < 1:
            await ctx.send(f"{ctx.author.mention}, you have to give me some roles to add...")
            return

        new_requestable_roles: typing.List[discord.Role] = []
        for role_name in role_names:
            role: discord.Role = discord.utils.find(lambda r: r.name.upper() == role_name.upper(), ctx.guild.roles)

            if role is None:
                raise NoSuchRoleError(role_name)

            self.db.roles.put(role)
            new_requestable_roles.append(role)

        new_roles_msg: typing.List[str] = [f"`{role.name}`" for role in new_requestable_roles]
        new_roles_msg: str = ', '.join(new_roles_msg)
        await ctx.send(f"{ctx.author.mention}, the following roles can now be requested here: {new_roles_msg}")

    @WegbotCog.is_mod()
    @cmd.command("remove", hidden=True)
    async def remove(self, ctx: commands.Context, *, role_name: str):
        """ Remove a requestable role from the database """
        role: discord.Role = discord.utils.find(lambda r: r.name.upper() == role_name.upper(), ctx.guild.roles)

        if role is None:
            raise NoSuchRoleError(role_name)

        self.db.roles.remove(role)
        await ctx.send(f"{ctx.author.mention}, `{role.name}` can now **no longer** be requested here.")

    @WegbotCog.is_mod()
    @cmd.command("clear", hidden=True)
    async def clear(self, ctx: commands.Context):
        """ Clear all requestable roles from the database """
        self.db.roles.clear(ctx.guild)

        roles_left: int = self.db.roles.count(ctx.guild)
        if not roles_left == 0:
            raise RolesNotClearedError(ctx.guild)

        await ctx.send(f"{ctx.author.mention}, i have cleared all requestable roles from this server.")
