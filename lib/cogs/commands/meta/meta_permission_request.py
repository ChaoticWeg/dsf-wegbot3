from discord.ext import commands
from lib.cogs.base import WegbotCog


class MetaPermissionRequestCog(WegbotCog, name="MetaPermissionRequest", command_attrs=dict(hidden=True)):

    @commands.is_owner()
    @commands.guild_only()
    @WegbotCog.has_table("permission_requests")
    @commands.group("pr", aliases=["fake-request"])
    async def cmd(self, ctx: commands.Context, permission_name: str):
        await self.bot.request_permission(ctx.channel, permission_name)
