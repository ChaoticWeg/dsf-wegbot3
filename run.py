import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs import cog_names
from extensions import extension_names

load_dotenv()

bot = commands.Bot(command_prefix=os.getenv("COMMAND_PREFIX", "?"))

for c_name in cog_names:
    print(f"loading {c_name}")
    bot.load_extension(c_name)

for x_name in extension_names:
    print(f"loading {x_name}")
    bot.load_extension(x_name)


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="discord.py rewrite"))


if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN", None)
    if token is None:
        raise RuntimeError("BOT_TOKEN environment variable is REQUIRED to run the bot")
    bot.run(token)
