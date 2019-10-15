import discord

from lib.cogs.base import WegbotCog


class PinnerCog(WegbotCog, name="Pinner"):
    """ Pins and archives messages that receive enough pin reacts """

    default_threshold = 3

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
            except discord.Forbidden:
                # unable to pin - need Manage Messages permission in this channel
                print(f"pinner: {guild.name} :: lack manage_messages permission in #{reaction.message.channel.name}")
                await self.notify_lacking_permissions(reaction.message.channel)

            # TODO: build embed and find somewhere to dump it

    async def notify_lacking_permissions(self, channel: discord.TextChannel):
        """ Notify the admins of this server that the bot does not have proper permissions to pin """

        # get admin channel
        guild: discord.Guild = channel.guild
        admin_channel: discord.TextChannel = self.db.admin_channel.get(guild)

        if admin_channel is None:
            # no admin channel, cannot notify

            print(f"pinner: {guild.name} :: no admin channel linked; unable to bug guild admins for permission")
            return

        # explicitly mention bot owner (me) if a member of the server and can see admin channel,
        # else default to guild owner
        target_member: discord.Member = discord.utils.get(guild.members, id=self.bot.owner_id)
        target_member = (
            target_member if target_member is not None and admin_channel.permissions_for(target_member).read_messages
            else guild.owner
        )

        # admin channel exists, notify
        await admin_channel.send(
            f"{target_member.mention}, i need the 'Manage Messages' permission to pin a message in " +
            f"{channel.mention} and i'm bugging you for it now. if you don't want to give " +
            "me this permission that's okay; just revoke my 'Read Messages' permission to disable pinning in " +
            f"{channel.mention}."
        )
