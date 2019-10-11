from lib.wegbot import Wegbot
from .pinner import PinnerCog


def setup(bot: Wegbot):
    bot.add_cog(PinnerCog(bot))
