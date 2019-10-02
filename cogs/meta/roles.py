from discord.ext import commands
from .base_cog import MetaBaseCog

from ..errors import RoleNotFoundError, RoleAlreadyAddedError, RoleNotAddedError, \
    RoleNotRequestableError, RoleNotRemovedError, WegbotCommandError, AddingModRoleError
from ..utils.arrays import concat_array

import discord
import sqlite3


class MetaRolesCog(MetaBaseCog, name="MetaRoles", command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        super().__init__(bot)

    @commands.group(name="roles")
    @commands.is_owner()
    @commands.guild_only()
    async def base_cmd(self, ctx: commands.Context):
        await ctx.trigger_typing()
        if ctx.invoked_subcommand is None:
            await ctx.send("what _about_ the roles")

    @base_cmd.command(name="list")
    async def list_roles(self, ctx: commands.Context):
        """ List the requestable roles in this server """
        await ctx.trigger_typing()

        role_ids = self.db.roles.get_all(ctx.guild)
        if len(role_ids) < 1:
            await ctx.send("there are no requestable roles in this server.")
        else:
            roles = [discord.utils.find(lambda r: str(r.id) == str(r_id), ctx.guild.roles) for r_id in role_ids]
            role_names = [r.name for r in roles if r is not None]
            await ctx.send(f"the following roles are requestable here: {concat_array(role_names)}")

    @base_cmd.command(name="add")
    async def add_role(self, ctx: commands.Context, *, role_name: str):
        """ Mark a role as requestable in this server """
        await ctx.trigger_typing()

        role = discord.utils.find(lambda r: r.name == role_name, ctx.guild.roles)
        if role is None:
            raise RoleNotFoundError(role_name)

        if self.db.roles.has(role):
            raise RoleAlreadyAddedError(role.name)

        if self.db.mods.has(role):
            raise AddingModRoleError(role.name)

        self.db.roles.add(role)

        if not self.db.roles.has(role):
            raise RoleNotAddedError(role.name)

        await ctx.send(f"success: role `{role.name}` is now requestable in this server")

    @base_cmd.command(name="remove")
    async def remove_role(self, ctx: commands.Context, *, role_name: str):
        """ Revoke the ability to request a given role in this server """
        await ctx.trigger_typing()

        role = discord.utils.find(lambda r: r.name == role_name, ctx.guild.roles)
        if role is None:
            raise RoleNotFoundError(role_name)

        if not self.db.roles.has(role):
            raise RoleNotRequestableError(role.name)

        self.db.roles.remove(role)

        if self.db.roles.has(role):
            raise RoleNotRemovedError(role.name)

        await ctx.send(f"success: role `{role.name}` is no longer requestable in this server")

    @base_cmd.command(name="clear")
    async def clear_roles(self, ctx: commands.Context):
        """ Remove all requestable roles in this server """
        await ctx.trigger_typing()

        self.db.roles.clear(ctx.guild)
        new_roles_count = len(self.db.roles.get_all(ctx.guild))

        await ctx.send(f"success: there are now {new_roles_count} requestable roles in this server")

    @base_cmd.error
    @add_role.error
    @remove_role.error
    @clear_roles.error
    @list_roles.error
    async def cog_error(self, ctx: commands.Context, error: discord.DiscordException):
        if isinstance(error, WegbotCommandError):
            await ctx.send(str(error))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("_which_ role tho")
        elif isinstance(error, sqlite3.IntegrityError):
            await ctx.send("you fucked up some database thing, go fix it nerd")
        else:
            await ctx.send("something weird went wrong; check the logs")
            print(error)
