from discord.ext.commands import Bot
from .bro import bro_factory


def setup(bot: Bot):
    bot.add_listener(bro_factory(bot), "on_message")
