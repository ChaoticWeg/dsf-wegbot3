import discord
from discord.ext import commands

from .. import utils


class ActivityCog(commands.Cog, name="Activity", command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="activity")
    @commands.is_owner()
    @commands.dm_only()
    async def set_activity(self, ctx, *, name: str):
        first_word = name.split(" ")[0]
        name_maybe = " ".join(name.split(" ")[1:])
        activity_type = utils.get_activity_type_by_name(first_word)
        is_valid_type = utils.is_activity_type(first_word)

        activity = utils.create_activity(name_maybe, activity_type) if is_valid_type else utils.create_activity(name)
        print(f"changing activity to \"{name}\"")
        await self._bot.change_presence(activity=activity)

    @set_activity.error
    async def set_activity_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("why are you bullying me")
            await ctx.author.send("dm me instead bb")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("don't tell me what to do.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("something doesn't check out but i'm not sure what...")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("yeah what about it")
        elif isinstance(error, discord.InvalidArgument):
            await ctx.send("discord doesn't seem to think that's a game")
        else:
            await ctx.send(f"something went horribly wrong ({type(error).__name__})")


def setup(bot):
    bot.add_cog(ActivityCog(bot))
