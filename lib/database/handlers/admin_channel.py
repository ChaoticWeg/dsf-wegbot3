from pathlib import Path

import discord

from .base import DatabaseHandler


class AdminChannelHandler(DatabaseHandler):
    """ Handles the admin_channel table, where admin channels are stored """

    table_name = "admin_channel"
    table_schema = "channel_id TEXT NOT NULL UNIQUE, guild_id TEXT NOT NULL UNIQUE"

    def __init__(self, db_file: Path):
        super().__init__(db_file, AdminChannelHandler.table_name, AdminChannelHandler.table_schema)

    def get(self, guild: discord.Guild):
        cur = self.db.cursor()
        cur.execute("SELECT channel_id FROM admin_channel WHERE guild_id = ?", (str(guild.id),))
        fetched: list = cur.fetchone()
        if fetched is None or len(fetched) == 0:
            print(f"database: {guild.name} :: guild has no admin channel set")
            return None
        channel_id: str = fetched[0]
        channel: discord.TextChannel = discord.utils.find(lambda c: str(c.id) == channel_id, guild.channels)
        if channel is None:
            print(f"database: {guild.name} :: invalid or deleted admin channel, advise deleting")
        print(f"database: {guild.name} :: admin channel is '{channel.name}'")
        return channel

    def set(self, channel: discord.TextChannel):
        print(f"database: {channel.guild.name} :: setting admin channel to '{channel.name}'")
        self.db.execute("INSERT OR REPLACE INTO admin_channel (channel_id, guild_id) VALUES (?, ?)",
                        (str(channel.id), str(channel.guild.id)))
        self.db.commit()

    def has(self, guild: discord.Guild):
        return self.get(guild) is not None

    def delete(self, guild: discord.Guild):
        print(f"database: {guild.name} :: deleting admin channel")
        self.db.execute("DELETE FROM admin_channel WHERE guild_id = ?", (str(guild.id),))
        self.db.commit()
