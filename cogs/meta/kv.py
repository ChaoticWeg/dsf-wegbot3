from discord.ext import commands
from .base_cog import MetaBaseCog


class MetaKeyValueCog(MetaBaseCog, name="MetaKV", command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        super().__init__(bot)

    @commands.group(name="kv")
    @commands.is_owner()
    @commands.guild_only()
    async def base_cmd(self, ctx: commands.Context):
        await ctx.trigger_typing()
        if ctx.invoked_subcommand is None:
            await ctx.send("yeah what about it")

    @base_cmd.command(name="set")
    async def set(self, ctx: commands.Context, key: str, *, value: str):
        await ctx.trigger_typing()

        self.db.misc.set(ctx.guild, key, value)
        new_value = self.db.misc.get(ctx.guild, key, default=None)

        await ctx.send(f"success: set `{key}` to `{new_value}`")

    @base_cmd.command(name="get")
    async def get(self, ctx: commands.Context, key: str):
        await ctx.trigger_typing()
        value = self.db.misc.get(ctx.guild, key)
        if value is None:
            await ctx.send(f"there's no key here called `{key}`")
        else:
            await ctx.send(f"`{key}` is set to `{value}`")

    @base_cmd.command(name="list")
    async def list(self, ctx: commands.Context):
        await ctx.trigger_typing()
        pairs = self.db.misc.get_all(ctx.guild)
        if pairs is None or len(pairs) == 0:
            await ctx.send("there are no k/v pairs for this server")
        else:
            lines = "\n".join([f"{c[0]}: {c[1]}" for c in pairs])
            await ctx.send(f"k/v pairs for **{ctx.guild.name}**:\n```\n{lines}\n```")

    @base_cmd.command(name="remove")
    async def remove(self, ctx: commands.Context, key: str):
        await ctx.trigger_typing()
        self.db.misc.remove(ctx.guild, key)
        await ctx.send(f"removed key `{key}` from this server")
