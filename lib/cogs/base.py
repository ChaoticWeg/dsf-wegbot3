import sqlite3

from discord.ext.commands import check, Cog, Context, CheckFailure, NotOwner, NoPrivateMessage

from ..errors.base import WegbotException
from ..errors.checks import InvalidTableError
from ..errors.database import DatabaseNotReachableError, WegbotDatabaseError
from ..wegbot import Wegbot


class WegbotCog(Cog):
    def __init__(self, bot: Wegbot):
        self.db: sqlite3.Connection = bot.db.connect()

    def cog_unload(self):
        self.db.close()

    @staticmethod
    def has_table(tablename: str):
        def check_table(ctx: Context):
            bot: Wegbot = ctx.bot
            if not bot.db.check_table(tablename):
                raise InvalidTableError(ctx.command, tablename)
            return True
        return check(check_table)

    async def cog_command_error(self, ctx, error):
        """ Gracefully handle errors that might arise from command errors """
        print(f"command error in {self.__class__.__name__}: {error}")

        if isinstance(error, DatabaseNotReachableError):
            await ctx.send(f"{ctx.author.mention}, i can't seem to reach my database right now.")
        elif isinstance(error, InvalidTableError):
            await ctx.send(f"{ctx.author.mention}, tell weg i can't reach the `{error.tablename}` table")
        elif isinstance(error, WegbotDatabaseError):
            await ctx.send(f"{ctx.author.mention}, i had some sort of database error.")
        elif isinstance(error, WegbotException):
            await ctx.send(f"{ctx.author.mention}, i had some sort of error that weg forgot about.")
        elif isinstance(error, NotOwner):
            await ctx.send(f"{ctx.author.mention}, that command is only available to weg.")
        elif isinstance(error, NoPrivateMessage):
            await ctx.send(f"you can't use that command in a DM.")
        elif isinstance(error, CheckFailure):
            await ctx.send(f"{ctx.author.mention}, one or more command checks failed, so i can't respond to that.")
        else:
            await ctx.send(f"{ctx.author.mention}, some sort of horrible error happened. i logged it for weg.")
            print("WHY DIDNT YOU HANDLE THIS LOL")
