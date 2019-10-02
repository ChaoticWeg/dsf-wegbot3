from discord.ext.commands import Bot
from .response import ping_response_factory


def setup(bot: Bot):
    bot.add_listener(ping_response_factory(bot), "on_message")
