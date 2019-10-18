import discord

from lib.cogs.base import WegbotCog


class PinnerCog(WegbotCog, name="Pinner"):
    """ Pins and archives messages that receive enough pin reacts """

    default_threshold = 3

    @WegbotCog.has_table("permission_requests")
    @WegbotCog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, _user):
        """ Pin a message if it gets enough pin reacts """

        # ignore pinned messages and reacts that aren't a pin
        if reaction.message.pinned or not str(reaction.emoji) == "📌":
            return

        guild: discord.Guild = reaction.message.guild
        threshold_str = self.db.key_value.get("pin_threshold", guild, default=str(PinnerCog.default_threshold))
        threshold = int(threshold_str)

        if reaction.count >= threshold:

            # try to pin, and notify if lacking permission

            try:
                await reaction.message.pin()
            except discord.Forbidden as e:
                # unable to pin - need Manage Messages permission in this channel
                print(f"pinner: {guild.name} :: lack manage_messages permission in #{reaction.message.channel.name}")
                print(f"pinner: DEBUG - {e.response.status} {e.response.reason} [{e.code}] - {e.text}")
                await self.bot.request_permission(reaction.message.channel, "manage_messages")

            # TODO: build embed and find somewhere to dump it
