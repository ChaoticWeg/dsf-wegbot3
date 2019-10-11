from pathlib import Path

import discord

from .base import DatabaseHandler


class KeyValueHandler(DatabaseHandler):
    def __init__(self, db_file: Path):
        super().__init__(db_file, "key_value",
                         "key TEXT NOT NULL, value TEXT, guild_id TEXT NOT NULL, UNIQUE(key, guild_id)")

    def get(self, key: str, guild: discord.Guild, default=None):
        cur = self.db.cursor()
        cur.execute("SELECT value FROM key_value WHERE key = ? AND guild_id = ?", (key, str(guild.id)))
        fetched: list = cur.fetchone()
        if fetched is None or len(fetched) == 0:
            print(f"database: {guild.name} :: {key} = {default} [default]")
            return default
        value = fetched[0]
        print(f"database: {guild.name} :: {key} = {value}")
        return value

    def has(self, key: str, guild: discord.Guild):
        return self.get(key, guild, default=None) is not None

    def set(self, key: str, value: str, guild: discord.Guild):
        print(f"database: {guild.name} :: setting '{key}' to '{value}'")
        self.db.execute("INSERT OR REPLACE INTO key_value (key, value, guild_id) VALUES (?, ?, ?)",
                        (key, value, str(guild.id)))
        self.db.commit()

    def delete(self, key: str, guild: discord.Guild):
        print(f"database: {guild.name} :: clearing value for '{key}'")
        self.db.execute("DELETE FROM key_value WHERE key = ? AND guild_id = ?", (key, str(guild.id)))
        self.db.commit()

    def get_all(self, guild: discord.Guild):
        print(f"database: {guild.name} :: getting ALL key/value pairs")
        cur = self.db.cursor()
        cur.execute("SELECT key, value FROM key_value WHERE guild_id = ? ORDER BY key ASC", (str(guild.id),))
        result = [dict(key=c[0], value=c[1]) for c in cur.fetchall()]
        print(f"database: {guild.name} :: found {len(result)} k/v pairs")
        return result

    def clear(self, guild: discord.Guild):
        print(f"database: {guild.name} :: clearing all k/v pairs")
        self.db.execute("DELETE FROM key_value WHERE guild_id = ?", (str(guild.id),))
        self.db.commit()
