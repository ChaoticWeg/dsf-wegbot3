import sqlite3

from discord.ext import commands

from ..errors.base import WegbotException
from ..errors.checks import InvalidTableError
from ..errors.database import DatabaseNotReachableError, WegbotDatabaseError
from ..wegbot import Wegbot


class WegbotCog(commands.Cog):
    def __init__(self, bot: Wegbot):
        self.db: sqlite3.Connection = bot.db.connect()

    def cog_unload(self):
        self.db.close()

    @staticmethod
    def has_table(tablename: str):
        def check_table(ctx: commands.Context):
            bot: Wegbot = ctx.bot
            if not bot.db.check_table(tablename):
                raise InvalidTableError(ctx.command, tablename)
            return True
        return commands.check(check_table)

    async def cog_command_error(self, ctx, error):
        """ Gracefully handle errors that might arise from command errors """
        print(f"command error in {self.__class__.__name__}: {error}")

        # wegbot errors
        if isinstance(error, DatabaseNotReachableError):
            await ctx.send(f"{ctx.author.mention}, i can't seem to reach my database right now.")
        elif isinstance(error, WegbotDatabaseError):
            await ctx.send(f"{ctx.author.mention}, i had some sort of database error.")
            print(error)
        elif isinstance(error, WegbotException):
            await ctx.send(f"{ctx.author.mention}, i had some sort of error that weg forgot about.")
            print(error)

        # check failures
        elif isinstance(error, InvalidTableError):
            await ctx.send(f"{ctx.author.mention}, tell weg i can't reach the `{error.tablename}` table")
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"{ctx.author.mention}, that command is only available to weg.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(f"you can't use that command in a DM.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention}, one or more command checks failed, so i can't respond to that.")

        # command errors
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, you're missing a required argument. use `?help` if you need it.")
        elif isinstance(error, commands.CommandError):
            await ctx.send(f"{ctx.author.mention}, tell weg he needs to handle `{error.__class__.__name__}` errors.")

        # weird shit
        else:
            await ctx.send(f"{ctx.author.mention}, some sort of horrible error happened. i logged it for weg.")
            print(error)
            print("WHY DIDNT YOU HANDLE THIS LOL")
