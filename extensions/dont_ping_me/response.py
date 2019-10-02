import discord
from discord.ext import commands


def ping_response_factory(bot: commands.Bot):
    async def respond_to_ping(message: discord.Message):
        if message.author.bot:
            return

        if len([u for u in message.mentions if u.id == bot.user.id]) > 0:
            # we have been  s u m m o n e d
            ping_emoji = discord.utils.get(message.guild.emojis, name="ping")
            if ping_emoji is not None:
                await message.add_reaction(ping_emoji)

    return respond_to_ping
