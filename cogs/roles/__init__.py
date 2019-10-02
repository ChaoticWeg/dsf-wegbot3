import discord
from discord.ext import commands

from ..db import DatabaseHandlingCog
from ..utils.arrays import concat_array


def build_addrole_denial_message(role_name, roles_already_given, adding_all):
    # no roles to add
    if adding_all:
        # already has all the roles
        return "you already have all of the roles"
    elif len(roles_already_given) > 1:
        # requested role(s) already given
        return f"you already have all of those roles"
    else:
        # requested one or more roles that don't exist
        return "those roles don't exist" if len(role_name.split(",")) > 1 else "that role doesn't exist"


def build_addrole_approval_message(roles_to_add, roles_already_given):
    msg = ""

    if len(roles_already_given) > 0:
        msg += f"you already had {concat_array(roles_already_given)}, but "

    return msg + f"i just gave you {concat_array(roles_to_add)}."


class RolesCog(DatabaseHandlingCog, name="Roles"):

    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="addrole")
    @commands.guild_only()
    async def addrole(self, ctx: commands.Context, *, role_name: str):
        """ Request a role or roles in this server """
        await ctx.trigger_typing()
        adding_all = False
        requestable_role_ids = self.db.roles.get_all(ctx.guild)

        if role_name == "all":
            # get all requestable roles from the database and give the ones that the author doesn't already have
            adding_all = True
            author_role_ids = [str(r.id) for r in ctx.author.roles]
            remaining_ids = [r_id for r_id in requestable_role_ids if r_id not in author_role_ids]
            roles_to_add = [discord.utils.find(lambda r: str(r.id) == rid, ctx.guild.roles) for rid in remaining_ids]

        else:
            # the author is requesting specific role(s)
            role_names = [n.strip() for n in role_name.split(",")]
            roles_raw = [discord.utils.get(ctx.guild.roles, name=rn) for rn in role_names]

            # check that all names are valid
            invalid_names = [n for n in role_names if n not in [r.name for r in roles_raw if r is not None]]
            if len(invalid_names) > 0:
                await ctx.send(
                    f"{ctx.author.mention}, {concat_array(invalid_names)} " +
                    ("are not valid roles" if len(invalid_names) > 1 else "is not a valid role")
                )
                return

            # check that all roles are requestable
            nonrequestable_roles = [r for r in roles_raw if r is not None and str(r.id) not in requestable_role_ids]
            if len(nonrequestable_roles) > 0:
                await ctx.send(
                    f"{ctx.author.mention}, {concat_array(nonrequestable_roles)} " +
                    ("are not requestable roles" if len(invalid_names) > 1 else "is not a requestable role")
                )
                return

            roles_to_add = [n for n in roles_raw if n is not None]

        # separate out the roles that the author already has
        roles_already_given = [r for r in roles_to_add if r in ctx.author.roles]
        roles_to_add = [r for r in roles_to_add if r not in roles_already_given]

        if len(roles_to_add) == 0:
            # no roles to add, tell them why
            msg = build_addrole_denial_message(role_name, roles_already_given, adding_all)
            await ctx.send(f"{ctx.author.mention}, {msg}")

        else:
            # we have roles to add, let them know
            await ctx.author.add_roles(*roles_to_add, reason=f"Requested via ?addrole by {ctx.author}")
            msg = build_addrole_approval_message(roles_to_add, roles_already_given)
            await ctx.send(f"{ctx.author.mention}, {msg}")

    @commands.command(name="removerole")
    @commands.guild_only()
    async def removerole(self, ctx: commands.Context, *, role_name: str):
        """ Remove a role from yourself """
        await ctx.trigger_typing()
        requestable_role_ids = self.db.roles.get_all(ctx.guild)

        if role_name == "all":
            author_roles = [str(r.id) for r in ctx.author.roles if str(r.id) in requestable_role_ids]
            roles_to_remove = [discord.utils.find(lambda r: str(r.id) == rid, ctx.guild.roles) for rid in author_roles]

        else:
            role_names = [n.strip() for n in role_name.split(",")]
            roles_raw = [discord.utils.find(lambda r: r.name == n, ctx.guild.roles) for n in role_names]

            # check that all roles are valid
            invalid_names = [n for n in role_names if n not in [r.name for r in roles_raw if r is not None]]
            if len(invalid_names) > 0:
                await ctx.send(
                    f"{ctx.author.mention}, {concat_array(invalid_names)} " +
                    ("are not valid roles" if len(invalid_names) > 1 else "is not a valid role")
                )
                return

            # check that all roles are requestable
            nonrequestable_names = [r.name for r in roles_raw if str(r.id) not in requestable_role_ids]
            if len(nonrequestable_names) > 0:
                await ctx.send(
                    f"{ctx.author.mention}, {concat_array(nonrequestable_names)} " +
                    ("are not requestable roles" if len(nonrequestable_names) > 1 else "is not a requestable role")
                )
                return

            roles_to_remove = [r for r in roles_raw if r is not None]

        if len(roles_to_remove) == 0:
            await ctx.send(f"{ctx.author.mention}, you don't have any requestable roles for me to remove")
            return

        await ctx.author.remove_roles(*roles_to_remove, reason=f"Requested via ?removerole by {ctx.author}")
        await ctx.send(f"{ctx.author.mention}, i just removed {concat_array(roles_to_remove)} from you")

    @addrole.error
    @removerole.error
    async def addrole_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("you can't request a role from a DM")
            print(error)
        elif isinstance(error, commands.CommandError):
            await ctx.send(f"{ctx.author.mention}, {str(error)}")
        else:
            await ctx.send(f"something happened (`{type(error).__name__}`). tell weg to check the logs")
            print(error)


def setup(bot):
    bot.add_cog(RolesCog(bot))
