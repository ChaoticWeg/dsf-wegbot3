from datetime import datetime

import discord
from discord.ext import commands

from ..base import WegbotCog


class MetaKeyValueCog(WegbotCog, name="MetaKeyValue", command_attrs=dict(hidden=True)):

    @commands.is_owner()
    @WegbotCog.has_table("key_value")
    @commands.group("kv")
    async def cmd(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.list.invoke(ctx)
            return

    @cmd.command("list")
    async def list(self, ctx: commands.Context):
        await ctx.trigger_typing()

        pairs = self.db.key_value.get_all(ctx.guild)

        pairs_descriptions = [f"**{p.get('key')}** : **{p.get('value')}**" for p in pairs]
        pairs_summary = "\n".join(pairs_descriptions) if len(pairs_descriptions) > 0 else "**(none)**"

        embed = discord.Embed(
            timestamp=datetime.now(),
            description=f"{pairs_summary}"
        )

        embed.set_author(name=f"Key/value pairs in {ctx.guild.name}", icon_url=ctx.guild.icon_url)
        embed.set_footer(text="Powered by discord.py", icon_url="https://projects.chaoticweg.cc/supereyes.png")

        await ctx.send(embed=embed)

    @cmd.command("set")
    async def set(self, ctx: commands.Context, key: str, *, value: str):
        await ctx.trigger_typing()
        self.db.key_value.set(key, value, ctx.guild)
        new_value = self.db.key_value.get(key, ctx.guild)
        await ctx.send(f"{ctx.author.mention}, `{key}` is now set to `{new_value}`")

    @cmd.command("get")
    async def get(self, ctx: commands.Context, *, key: str):
        await ctx.trigger_typing()
        value = self.db.key_value.get(key, ctx.guild)
        await ctx.send(f"{ctx.author.mention}, `{key}` is set to `{value}`")

    @cmd.command("clear")
    async def clear(self, ctx: commands.Context):
        await ctx.trigger_typing()
        self.db.key_value.clear(ctx.guild)
        await ctx.send(f"{ctx.author.mention}, i have cleared all k/v pairs for this guild")
