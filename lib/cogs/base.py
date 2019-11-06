from discord.ext import commands

from ..database import WegbotDatabase
from ..errors.base import WegbotException
from ..errors.checks import InvalidTableError, MemberIsNotModError, WegbotCheckFailure
from ..errors.commands import CommandNotImplementedError, WegbotCommandError
from ..errors.database import DatabaseNotReachableError, WegbotDatabaseError
from ..wegbot import Wegbot


class WegbotCog(commands.Cog):
    def __init__(self, bot: Wegbot):
        self.bot = bot
        self.db: WegbotDatabase = bot.db

    @staticmethod
    def has_table(tablename: str):
        def check_table(ctx: commands.Context):
            bot: Wegbot = ctx.bot
            if not bot.db.check_table(tablename):
                raise InvalidTableError(ctx.command, tablename)
            return True
        return commands.check(check_table)

    @staticmethod
    def is_mod():
        def check_mod(ctx: commands.Context):
            bot: Wegbot = ctx.bot
            if not bot.db.check_mod(ctx.author):
                raise MemberIsNotModError(ctx.command, ctx.author)
            return True
        return commands.check(check_mod)

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
            await ctx.send(f"{ctx.author.mention}, tell weg i can't reach the `{error.tablename}` table.")
        elif isinstance(error, MemberIsNotModError):
            await ctx.send(f"{ctx.author.mention}, you have to be a mod to use that command.")
        elif isinstance(error, WegbotCheckFailure):
            await ctx.send(f"{ctx.author.mention}, tell weg that he forgot to handle `{error.__class__.__name__}`s.")
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"{ctx.author.mention}, that command is only available to weg.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(f"you can't use that command in a DM.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention}, one or more command checks failed, so i can't respond to that.")

        # command errors
        elif isinstance(error, CommandNotImplementedError):
            await ctx.send(f"{ctx.author.mention}, weg hasn't finished implementing that command yet.")
        elif isinstance(error, WegbotCommandError):
            await ctx.send(f"{ctx.author.mention}, {error}.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, you're missing a required argument. use `?help` if you need it.")
        elif isinstance(error, commands.CommandError):
            await ctx.send(f"{ctx.author.mention}, tell weg he needs to handle `{error.__class__.__name__}`s.")

        # weird shit
        else:
            await ctx.send(f"{ctx.author.mention}, some sort of horrible error happened. "
                           "i logged it for weg and berated him for it.")
            print(error)
            print("WHY DIDNT YOU HANDLE THIS LOL")
