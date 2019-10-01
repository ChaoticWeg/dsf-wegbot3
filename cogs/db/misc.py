from pathlib import Path
from .handler import DatabaseHandler

import discord
import sqlite3


class MiscHandler(DatabaseHandler):
    def __init__(self, dbfs_root: Path):
        super().__init__(dbfs_root, "misc")

    def on_initialize(self):
        cur = self._db.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM misc")
            count = cur.fetchone()[0]
            print(f"database: {count} miscellaneous key/value pairs")
        except sqlite3.OperationalError:
            cur.execute("CREATE TABLE misc (key text NOT NULL UNIQUE, value text, guild_id text NOT NULL)")
            self._db.commit()
            print(f"database: created new miscellaneous key/value table")

    def set(self, guild: discord.Guild, key: str, value: str):
        cur = self._db.cursor()
        guild_id = str(guild.id)
        try:
            cur.execute("INSERT INTO misc (key, value, guild_id) VALUES (?,?,?)", (key, value, guild_id))
            self._db.commit()
            print(f"database: inserted new key/value pair for guild '{guild.name}': {key} = {value}")
        except sqlite3.IntegrityError:
            cur.execute("UPDATE misc SET value = ? WHERE key = ? AND guild_id = ?", (value, key, guild_id))
            self._db.commit()
            print(f"database: updated key/value pair for guild '{guild.name}': {key} = {value}")

    def get(self, guild: discord.Guild, key: str, default=None):
        cur = self._db.cursor()
        try:
            cur.execute("SELECT value FROM misc WHERE key = ? AND guild_id = ?", (key, guild.id))
            result = cur.fetchone()
            result = result[0] if result is not None and len(result) > 0 else default
            print(f"database: fetched key/value pair for guild '{guild.name}': {key} = {result}")
            return result
        except Exception as e:
            print(f"database: WARN {e}")
            return default

    def get_all(self, guild: discord.Guild):
        cur = self._db.cursor()
        guild_id = str(guild.id)
        try:
            cur.execute("SELECT key, value FROM misc WHERE guild_id = ? ORDER BY key ASC", (guild_id,))
            return cur.fetchall()
        except Exception as e:
            print(f"database: WARN {e}")
            return []

    def remove(self, guild: discord.Guild, key: str):
        cur = self._db.cursor()
        guild_id = str(guild.id)
        try:
            cur.execute("DELETE FROM misc WHERE key = ? AND guild_id = ?", (key, guild_id))
            self._db.commit()
            print(f"database: deleted key/value pair for guild '{guild.name}': {key}")
        except sqlite3.OperationalError:
            print(f"database: WARN attempted to delete non-existent key/value pair for guild '{guild.name}': {key}")
