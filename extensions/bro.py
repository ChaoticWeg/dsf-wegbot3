import discord
from datetime import datetime, timedelta

from cogs.db import DatabaseCog


def bro_factory(bot):
    async def respond_with_bro(message: discord.Message):
        if not message.author.bot and message.clean_content == "BRO":
            db: DatabaseCog = bot.get_cog("Database")
            now_ts = str(datetime.now().timestamp())
            last_bro = datetime.utcfromtimestamp(float(db.misc.get(message.guild, "last_bro", now_ts)))
            bro_cooldown = int(db.misc.get(message.guild, "bro_cooldown", default=15))

            delta: timedelta = datetime.fromtimestamp(message.created_at.timestamp()) - last_bro

            if delta >= timedelta(seconds=bro_cooldown):
                db.misc.set(message.guild, "last_bro", str(datetime.now().timestamp()))
                await message.channel.send("BRO")

            else:
                ping_emoji = discord.utils.get(message.guild.emojis, name="ping")
                if ping_emoji is not None:
                    await message.add_reaction(ping_emoji)

    return respond_with_bro


def setup(bot):
    bot.add_listener(bro_factory(bot), "on_message")
