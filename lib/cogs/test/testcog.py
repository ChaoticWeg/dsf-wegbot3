from discord.ext.commands import command, is_owner, guild_only

from ..base import WegbotCog


class TestCog(WegbotCog, name="Test", command_attrs=dict(hidden=True)):

    @is_owner()
    @guild_only()
    @command("test")
    async def test(self, ctx):
        await ctx.send(f"{ctx.author.mention}, all checks went ok")
