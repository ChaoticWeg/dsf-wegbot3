from .testcog import TestCog

from lib.wegbot import Wegbot


def setup(bot: Wegbot):
    bot.add_cog(TestCog(bot))
