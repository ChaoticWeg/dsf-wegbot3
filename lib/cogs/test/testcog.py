from typing import Optional

from discord import utils as discord_utils, Emoji
from discord.ext import commands

from lib.cogs.base import WegbotCog


class TestCog(WegbotCog, name="Test", command_attrs=dict(hidden=True)):

    @commands.is_owner()
    @commands.guild_only()
    @commands.group("test")
    async def test_cmd(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("usage: `?test table <tablename>`")

    @test_cmd.command("table")
    async def test_table(self, ctx: commands.Context, *, tablename: str):
        table_ok: bool = ctx.bot.db.check_table(tablename)
        emoji_name: str = "green_check" if table_ok else "red_x"
        react_emoji: Optional[Emoji] = discord_utils.get(ctx.guild.emojis, name=emoji_name)
        if react_emoji is not None:
            await ctx.message.add_reaction(react_emoji)
        else:
            emoji_fallback = "+1" if table_ok else "-1"
            await ctx.send(f"{ctx.author.mention}, :{emoji_fallback}:")
