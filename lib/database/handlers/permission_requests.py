from lib.database.handlers.base import DatabaseHandler

import discord
from datetime import datetime
from pathlib import Path


class PermissionRequestsHandler(DatabaseHandler):
    """ Keeps track of permission requests, to ensure we do not send too many duplicates. """

    tablename: str = "permission_requests"
    schema: str = "channel_id TEXT NOT NULL, permission_name TEXT NOT NULL, timestamp TEXT NOT NULL, " + \
                  "UNIQUE(channel_id, permission_name)"

    def __init__(self, db_file: Path):
        super().__init__(db_file, PermissionRequestsHandler.tablename, PermissionRequestsHandler.schema)

    def get(self, channel: discord.TextChannel, perm: str):
        """ Retrieves a :class:`datetime.datetime` representing the last time this permission
        was requested for this channel """
        print(f"database: {channel.guild.name} :: checking last permission request for '{perm}' in '#{channel.name}'")
        cur = self.db.cursor()
        cur.execute("SELECT timestamp FROM permission_requests WHERE channel_id = ? AND permission_name = ?",
                    (str(channel.id), perm))
        fetched: list = cur.fetchone()
        if fetched is None or len(fetched) == 0:
            print(f"database: {channel.guild.name} :: permission '{perm}' not yet requested for '#{channel.name}'")
            return None
        value = fetched[0]
        print(f"database: {channel.guild.name} :: '{perm}' in '#{channel.name}' last requested: {value}")
        return datetime.utcfromtimestamp(float(value))

    def has(self, channel: discord.TextChannel, perm: str):
        return self.get(channel, perm) is not None

    def set(self, channel: discord.TextChannel, perm: str, when: datetime = datetime.utcnow()):
        print(f"database: {channel.guild.name} :: logging permission request for '{perm}' in '#{channel.name}'")
        sql_str = "INSERT OR REPLACE INTO permission_requests (channel_id, permission_name, timestamp) VALUES (?,?,?)"
        self.db.execute(sql_str, (str(channel.id), perm, str(when.timestamp())))
        self.db.commit()

    def delete(self, channel: discord.TextChannel, perm: str):
        print(f"database: {channel.guild.name} :: deleting last permission request for '{perm}' in '#{channel.name}'")
        sql_str = "DELETE FROM permission_requests WHERE channel_id = ? AND permission_name = ?"
        self.db.execute(sql_str, (str(channel.id), perm))
        self.db.commit()
