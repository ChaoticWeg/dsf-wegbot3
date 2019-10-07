from discord.ext.commands import Context, command, is_owner, guild_only
from discord import utils as discord_utils, Emoji

from ..base import WegbotCog


class TestCog(WegbotCog, name="Test", command_attrs=dict(hidden=True)):

    @is_owner()
    @guild_only()
    @command("test")
    async def test(self, ctx: Context):
        ok_emoji: Emoji = discord_utils.get(ctx.guild.emojis, name="green_check")
        if ok_emoji is not None:
            await ctx.message.add_reaction(ok_emoji)
        else:
            await ctx.send(":+1:")
