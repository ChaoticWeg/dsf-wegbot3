import discord

from lib.cogs.base import WegbotCog


class PinnerCog(WegbotCog, name="Pinner"):
    """ Pins and archives messages that receive enough pin reacts """

    default_threshold = 3

    @WegbotCog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, _user):
        """ Pin a message if it gets enough reacts """

        # ignore pinned messages and reacts that aren't a pin
        if reaction.message.pinned or not str(reaction.emoji) == "📌":
            return

        threshold_str = self.db.key_value.get("pin_threshold", reaction.message.guild,
                                              default=str(PinnerCog.default_threshold))
        threshold = int(threshold_str)

        if reaction.count >= threshold:
            # pin reacts are equal to or greater than threshold
            await reaction.message.pin()
            # TODO: build embed and find somewhere to dump it
