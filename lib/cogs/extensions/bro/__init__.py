from lib.wegbot import Wegbot
from .bro import BroCog


def setup(bot: Wegbot):
    bot.add_cog(BroCog(bot))
