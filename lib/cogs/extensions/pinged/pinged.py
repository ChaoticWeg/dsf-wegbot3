import random
from typing import Optional

import discord

from lib.cogs.base import WegbotCog


class PingedCog(WegbotCog, name="Pinged"):
    """ Respond to bot pings with an emoji """

    guild_emoji_prefix = "guild:"
    fallback_reaction = "👀"

    possible_reactions = [
        "guild:ping",
        "guild:supereyes",
        "guild:yeehaw",
        "guild:griffin",
        "guild:dab",
        "guild:fedoratip",
        "guild:redcard",
        "guild:woo",
        "guild:owo",
        "♿",
        "😎",
        "😤"
    ]

    @staticmethod
    def is_guild_emoji(emoji_str: str):
        """ Determine whether the emoji string is a guild emoji """
        prefix_len: int = len(PingedCog.guild_emoji_prefix)
        return len(emoji_str) > prefix_len and emoji_str[:prefix_len] == PingedCog.guild_emoji_prefix

    @staticmethod
    def get_guild_emoji_name(emoji_str: str):
        """ Get the guild emoji name if applicable, else return the string verbatim """
        return emoji_str[len(PingedCog.guild_emoji_prefix):] if PingedCog.is_guild_emoji(emoji_str) else emoji_str

    @staticmethod
    def get_emoji(guild: discord.Guild):
        """ Attempt to get one of a few emojis, gradually falling back to a Unicode emoji if none are found """
        emoji_str: str = random.choice(PingedCog.possible_reactions)

        # if it's a regular Unicode emoji, just return it
        if not PingedCog.is_guild_emoji(emoji_str):
            return emoji_str

        # it's a guild emoji, so attempt to retrieve it, and if unable then return the fallback reaction
        emoji_name: str = PingedCog.get_guild_emoji_name(emoji_str)
        emoji: Optional[discord.Emoji] = discord.utils.get(guild.emojis, name=emoji_name)
        if emoji is not None:
            return emoji

        # didn't find it, so returning fallback reaction
        print(f"pinged: {guild.name} :: unable to find reaction '{emoji_name}', defaulting to fallback")
        return PingedCog.fallback_reaction

    @WegbotCog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not self.bot.user.mentioned_in(message):
            return

        reaction = PingedCog.get_emoji(message.guild)
        await message.add_reaction(reaction)
