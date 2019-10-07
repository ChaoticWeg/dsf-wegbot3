from discord.ext.commands import Cog, CheckFailure, NotOwner, NoPrivateMessage

from ..database import WegbotDatabase
from ..wegbot import Wegbot

from ..errors.database import DatabaseNotReachableError, WegbotDatabaseError
from ..errors.base import WegbotException


class WegbotCog(Cog):
    def __init__(self, bot: Wegbot):
        self.db: WegbotDatabase = bot.db.connect()

    async def cog_check(self, ctx):
        """ Check that the database is reachable for every command and subcommand """
        if self.db is None:
            raise DatabaseNotReachableError(self.__class__.__name__)
        return True

    async def cog_command_error(self, ctx, error):
        """ Gracefully handle errors that might arise from command errors """
        print(f"command error in {self.__class__.__name__}: {error}")

        if isinstance(error, DatabaseNotReachableError):
            await ctx.send(f"{ctx.author.mention}, i can't seem to reach my database right now.")
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
