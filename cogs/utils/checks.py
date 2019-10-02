from discord.ext import commands

import discord


def is_mod():
    async def predicate(ctx: commands.Context):
        bot: commands.Bot = ctx.bot
        author: discord.Member = ctx.author
        db = bot.get_cog("Database")

        mod_roles = db.mods.get_all(ctx.guild)
        mod_role_ids = [str(r_id) for r_id in mod_roles]
        author_role_ids = [str(r.id) for r in author.roles]

        union = [r for r in mod_role_ids if r in author_role_ids]
        return len(union) > 0
    return commands.check(predicate)
