from discord.ext import commands
from lib.cogs.base import WegbotCog
from typing import Iterable

import discord


class RolesCog(WegbotCog, name="Roles"):
    """ Tools for requesting and relinquishing eligible roles """

    @staticmethod
    def parse_roles(ctx: commands.Context, roles: Iterable[str]):
        role_names = [r.strip() for r in roles]
        return [
            rnn for rnn in [
                discord.utils.find(lambda rn: rn.name.lower() == r.lower(), ctx.guild.roles) for r in role_names
            ] if rnn is not None
        ]

    @commands.guild_only()
    @commands.has_role("Verified")
    @WegbotCog.has_table("roles")
    @commands.group("addrole")
    async def addrole(self, ctx: commands.Context, *, role_name: str):
        """ Request a role by name, multiple roles by names separated with a comma, or ALL requestable roles """
        await ctx.trigger_typing()

        if ctx.invoked_subcommand is not None:
            return

        if role_name.lower() == "all":
            await self.add_all_roles.invoke(ctx)
            return

        roles = RolesCog.parse_roles(ctx, role_name.split(","))
        ineligible_roles = [r for r in roles if not self.db.roles.has(r)]

        if len(ineligible_roles) > 0:
            ineligible_names = [f"`{r.name}`" for r in ineligible_roles]
            plurality = "roles are" if len(ineligible_names) > 1 else "role is"
            await ctx.send(f"{ctx.author.mention}, the following {plurality} ineligible to be requested: "
                           + ", ".join(ineligible_names))
            return

        if len(roles) == 0:
            msg: str = f"{ctx.author.mention}, `{role_name}` doesn't match any roles."
            if " " in role_name.strip():
                msg += " separate multiple roles with a comma."
            await ctx.send(msg)
            return

        await ctx.author.add_roles(*roles, reason=f"Requested by {ctx.author} via ?addrole")
        await ctx.send(f"{ctx.author.mention}, i just gave you the following role(s): "
                       + ", ".join([f"`{r.name}`" for r in roles]))

    @addrole.command("all")
    async def add_all_roles(self, ctx: commands.Context):
        """ Special role: request all roles """
        member: discord.Member = ctx.author
        roles = self.db.roles.get_all(ctx.guild)
        await member.add_roles(*roles, reason=f"Requested by {member} via ?addrole")
        await ctx.send(f"{member.mention}, i just gave you all of the roles.")

    @commands.guild_only()
    @commands.has_role("Verified")
    @WegbotCog.has_table("roles")
    @commands.group("removerole")
    async def removerole(self, ctx: commands.Context, *, role_name: str):
        """ Relinquish a role by name, multiple roles by names separated with a comma, or ALL requestable roles """
        await ctx.trigger_typing()

        if ctx.invoked_subcommand is not None:
            return

        if role_name.lower() == "all":
            await self.remove_all_roles.invoke(ctx)
            return

        roles = RolesCog.parse_roles(ctx, role_name.split(","))
        ineligible_roles = [r for r in roles if not self.db.roles.has(r)]

        if len(ineligible_roles) > 0:
            ineligible_names = [f"`{r.name}`" for r in ineligible_roles]
            plurality = "roles are" if len(ineligible_names) > 1 else "role is"
            await ctx.send(f"{ctx.author.mention}, the following {plurality} ineligible to be requested: "
                           + ", ".join(ineligible_names))
            return

        if len(roles) == 0:
            msg: str = f"{ctx.author.mention}, `{role_name}` doesn't match any roles."
            if " " in role_name.strip():
                msg += " separate multiple roles with a comma."
            await ctx.send(msg)
            return

        await ctx.author.remove_roles(*roles, reason=f"Requested by {ctx.author} via ?removerole")
        await ctx.send(f"{ctx.author.mention}, i just took away following role(s): "
                       + ", ".join([f"`{r.name}`" for r in roles]))

    @removerole.command("all")
    async def remove_all_roles(self, ctx: commands.Context):
        """ Special role: relinquish all roles """
        member: discord.Member = ctx.author
        roles = self.db.roles.get_all(ctx.guild)
        await member.remove_roles(*roles, reason=f"Requested by {member} via ?removerole")
        await ctx.send(f"{member.mention}, i just took all of your roles.")
