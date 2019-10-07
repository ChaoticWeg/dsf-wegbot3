import os

from dotenv import load_dotenv

from lib.cogs import cog_names
from lib.wegbot import Wegbot

load_dotenv()

bot: Wegbot = Wegbot(command_prefix=os.getenv("COMMAND_PREFIX", "?"))

for c in cog_names:
    print(f"loading {c}")
    bot.load_extension(f"lib.{c}")


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")
    bot.db.initialize()


if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN", None)
    if token is None:
        raise RuntimeError("BOT_TOKEN environment variable is REQUIRED to run the bot")
    bot.run(token)
