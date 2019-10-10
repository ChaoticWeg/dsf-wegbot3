from datetime import datetime, timedelta
from discord.ext import commands
from lib.cogs.base import WegbotCog

import discord


class BroCog(WegbotCog, name="Bro"):
    """ BRO """

    triggers = [
        "bro",
        "ese",
        "hermano"
    ]

    def is_on_cooldown(self, guild: discord.Guild):
        now_dt: datetime = datetime.utcnow()

        last_bro_ts: str = self.db.key_value.get("last_bro", guild, default=None)
        print(f"BroCog: {guild.name} :: last_bro = {last_bro_ts}")
        if last_bro_ts is None:
            return False

        last_bro_dt: datetime = datetime.utcfromtimestamp(float(last_bro_ts))

        bro_cooldown_str: str = self.db.key_value.get("bro_cooldown", guild, default=str(10))

        since_last_bro: timedelta = now_dt - last_bro_dt
        print(f"BroCog: {guild.name} :: since last bro: {since_last_bro.seconds}")
        return since_last_bro < timedelta(seconds=int(bro_cooldown_str))

    @commands.Cog.listener("on_message")
    async def respond_with_bro(self, message: discord.Message):
        if message.author.bot:
            return

        if not message.clean_content.lower() in BroCog.triggers:
            return

        if self.is_on_cooldown(message.guild):
            react_emoji = discord.utils.get(message.guild.emojis, name="supereyes")
            await message.add_reaction(react_emoji if react_emoji is not None else "👀")
            return

        await message.channel.trigger_typing()
        this_bro = datetime.utcnow()
        self.db.key_value.set("last_bro", str(this_bro.timestamp()), message.guild)
        await message.channel.send(message.clean_content.upper())
