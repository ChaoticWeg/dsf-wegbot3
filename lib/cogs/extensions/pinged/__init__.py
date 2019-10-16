from lib.wegbot import Wegbot
from .pinged import PingedCog


def setup(bot: Wegbot):
    bot.add_cog(PingedCog(bot))
