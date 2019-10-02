import discord
from discord.ext import commands

from .base_cog import MetaBaseCog
from ..errors import RoleNotFoundError, RequestableRoleAsModError, RoleNotAddedError, RoleAlreadyAddedError, \
    RoleNotRemovedError, WegbotCommandError

from ..utils.arrays import concat_array
from ..utils.checks import is_mod


class MetaModsCog(MetaBaseCog, name="MetaMods", command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        super().__init__(bot)

    async def cog_command_error(self, ctx: commands.Context, error: discord.DiscordException):
        if isinstance(error, WegbotCommandError):
            await ctx.send(str(error))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("tell me more")
        elif isinstance(error, commands.CheckFailure):
            # this is probably already being handled, or at least it SHOULD be
            pass
        elif isinstance(error, commands.CommandError):
            print(f"cogs.meta: WARN UNHANDLED COMMANDERROR: {error}")
            await ctx.send(str(error))
        else:
            await ctx.send(f"something weird went wrong. tell weg i found a(n) {type(error).__name__} in cogs.meta")
            print(error)

    @commands.group(name="amiamod")
    @commands.guild_only()
    @is_mod()
    async def am_i_a_mod(self, ctx: commands.Context):
        """ I don't know, are you? """
        await ctx.trigger_typing()
        await ctx.send(f"{ctx.author.mention}, yes.")

    @am_i_a_mod.error
    async def i_am_not_mod(self, ctx: commands.Context, error: discord.DiscordException):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention}, no.")
        else:
            await ctx.send(f"{ctx.author.mention}, i don't know because there was an error (`{type(error).__name__}`")
            print(error)

    @commands.group(name="mods")
    @commands.is_owner()
    @commands.guild_only()
    async def base_cmd(self, ctx: commands.Context):
        """ fuck the mods """
        await ctx.trigger_typing()
        if ctx.invoked_subcommand is None:
            supereyes = discord.utils.get(ctx.guild.emojis, name="supereyes")
            await ctx.send(f"fuck the mods {supereyes if supereyes is not None else ''}")

    @base_cmd.command("add")
    async def add_role(self, ctx: commands.Context, *, role_name: str):
        """ Flag a role as moderator in this server """
        await ctx.trigger_typing()

        role = discord.utils.find(lambda r: r.name == role_name, ctx.guild.roles)
        if role is None:
            raise RoleNotFoundError(role_name)

        if self.db.roles.has(role):
            raise RequestableRoleAsModError(role.name)

        if self.db.mods.has(role):
            raise RoleAlreadyAddedError(role.name)

        self.db.mods.add(role)

        if not self.db.mods.has(role):
            raise RoleNotAddedError(role.name)

        await ctx.send(f"success: role `{role.name}` is now a mod role in this server")

    @base_cmd.command("remove")
    async def remove_role(self, ctx: commands.Context, *, role_name: str):
        """ Remove a mod role from this server """
        await ctx.trigger_typing()

        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None:
            raise RoleNotFoundError(role_name)

        if not self.db.mods.has(role):
            raise RoleNotAddedError(role.name)

        self.db.mods.remove(role)

        if self.db.mods.has(role):
            raise RoleNotRemovedError(role.name)

        await ctx.send(f"success: role `{role.name}` is no longer a mod role in this server")

    @base_cmd.command("clear")
    async def clear_roles(self, ctx: commands.Context):
        """ Clear all mod roles from this server """
        await ctx.trigger_typing()
        self.db.mods.clear(ctx.guild)
        await ctx.send(f"success: cleared all mod roles from this server")

    @base_cmd.command("list")
    async def list_roles(self, ctx: commands.Context):
        """ List mod roles in this server """
        await ctx.trigger_typing()

        role_ids = self.db.mods.get_all(ctx.guild)
        roles = [discord.utils.find(lambda r: str(r.id) == str(r_id), ctx.guild.roles) for r_id in role_ids]

        if len(roles) == 0:
            await ctx.send("there are no mod roles listed for this server")
        else:
            await ctx.send(f"mod roles in this server: `{concat_array([r.name for r in roles])}`")
