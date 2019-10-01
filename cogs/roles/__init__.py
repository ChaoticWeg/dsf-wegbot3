import discord
from discord.ext import commands

from ..db import DatabaseHandlingCog
from ..errors import RoleNotFoundError, RoleNotRequestableError, RoleAlreadyGivenError, RoleNeverGivenError


class RolesCog(DatabaseHandlingCog, name="Roles"):

    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="addrole")
    @commands.has_role("Verified")
    @commands.guild_only()
    async def addrole(self, ctx: commands.Context, *, role_name: str):
        """ Request a role in this server """
        async with ctx.typing():
            role: discord.Role = discord.utils.find(lambda r: r.name == role_name, ctx.guild.roles)

            if role.id in [r.id for r in ctx.author.roles]:
                raise RoleAlreadyGivenError(role.name)

            if role is None:
                raise RoleNotFoundError(role_name)

            if not self.db.roles.has(role):
                raise RoleNotRequestableError(role.name)

            await ctx.author.add_roles(role, reason=f"Requested by {ctx.author} via ?addrole")
            await ctx.send(f"{ctx.author.mention} i just gave you the role `{role.name}`")

    @commands.command(name="removerole")
    @commands.has_role("Verified")
    @commands.guild_only()
    async def removerole(self, ctx: commands.Context, *, role_name: str):
        """ Remove a role from yourself """
        async with ctx.typing():
            role: discord.Role = discord.utils.find(lambda r: r.name == role_name, ctx.guild.roles)

            if role.id not in [r.id for r in ctx.author.roles]:
                raise RoleNeverGivenError(role.name)

            if role is None:
                raise RoleNotFoundError(role_name)

            if not self.db.roles.has(role):
                raise RoleNotRequestableError(role.name)

            await ctx.author.remove_roles(role, reason=f"Requested by {ctx.author} via ?removerole")
            await ctx.send(f"{ctx.author.mention} i just removed the role `{role.name}` from you")

    @addrole.error
    @removerole.error
    async def addrole_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("something's not right. either you're not verified, or this is a DM. either way, no.")
        elif isinstance(error, commands.CommandError):
            await ctx.send(f"{ctx.author.mention}, {str(error)}")
        else:
            await ctx.send(f"something happened (`{type(error).__name__}`). tell weg to check the logs")
            print(error)


def setup(bot):
    bot.add_cog(RolesCog(bot))
