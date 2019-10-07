import os

import discord
from dotenv import load_dotenv

from lib.wegbot import Wegbot
from lib.cogs import cog_names

load_dotenv()

bot: Wegbot = Wegbot(command_prefix=os.getenv("COMMAND_PREFIX", "?"))

for c in cog_names:
    print(f"loading {c}")
    bot.load_extension(f"lib.{c}")


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="discord.py rewrite"))


if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN", None)
    if token is None:
        raise RuntimeError("BOT_TOKEN environment variable is REQUIRED to run the bot")
    bot.run(token)
