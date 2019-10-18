from datetime import datetime, timedelta

import discord
from discord.ext import commands

from lib.database import WegbotDatabase


class Wegbot(commands.Bot):
    """ Wegbot - subclass of discord.ext.commands.Bot """

    description: str = "Wegbot - resident idiot role-lord"
    version: str = "v3.0.2"
    default_activity: discord.Activity = discord.Game(name=f"wegbot {version} – ?help")

    permission_request_interval: timedelta = timedelta(hours=12)

    def __init__(self, command_prefix="?"):
        super().__init__(command_prefix, description=Wegbot.description, activity=Wegbot.default_activity)
        self.db: WegbotDatabase = WegbotDatabase()

    async def on_ready(self):
        print(f"logged in as {self.user}")
        self.db.initialize()

    async def request_permission(self, channel: discord.TextChannel, permission_name: str):
        """ Notify the admins of this server that the bot does not have proper permissions to pin """

        # check to make sure server has allowed permission requests
        can_bug: bool = self.db.key_value.get("request_permissions", channel.guild, default=False, transform=bool)
        if not can_bug:
            print(
                f"wegbot: {channel.guild.name} :: unable to request '{permission_name}' permission in " +
                f"'#{channel.name}' as the server has not allowed it"
            )
            return

        # check last time permissions were requested, to avoid duplicates
        last_request: datetime = self.db.permission_requests.get(channel, permission_name)
        if last_request is not None:
            time_since: timedelta = datetime.utcnow() - last_request
            if time_since < Wegbot.permission_request_interval:
                print(f"wegbot: {channel.guild.name} :: unable to request '{permission_name}' permission in " +
                      f"'#{channel.name}' as it was recently requested")
                return

        # get admin channel
        guild: discord.Guild = channel.guild
        admin_channel: discord.TextChannel = self.db.admin_channel.get(guild)

        if admin_channel is None:
            # no admin channel, cannot notify
            print(f"wegbot: {guild.name} :: no admin channel linked; unable to bug guild admins for permission")
            return

        await admin_channel.trigger_typing()

        # explicitly mention bot owner (me) if a member of the server and can see admin channel,
        # else default to guild owner
        target_member: discord.Member = discord.utils.get(guild.members, id=self.owner_id)
        target_member = (
            target_member if target_member is not None and admin_channel.permissions_for(
                target_member).read_messages
            else guild.owner
        )

        # log this request
        self.db.permission_requests.set(channel, permission_name)

        # admin channel exists, notify
        await admin_channel.send(
            f"{target_member.mention}, i need the `{permission_name}` permission in {channel.mention} and i'm " +
            "bugging you for it now."
        )
