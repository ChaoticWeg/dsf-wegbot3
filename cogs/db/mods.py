from pathlib import Path
from .handler import DatabaseHandler

import discord
import sqlite3


class ModsHandler(DatabaseHandler):
    def __init__(self, dbfs_root: Path):
        super().__init__(dbfs_root, "mods")

    def on_initialize(self):
        cur = self._db.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM mods")
            count = cur.fetchone()[0]
            print(f"database: {count} known mod roles")
        except sqlite3.OperationalError:
            cur.execute("CREATE TABLE mods (role_id text NOT NULL UNIQUE, guild_id text NOT NULL)")
            self._db.commit()
            print(f"database: created new mods table")

    def add(self, role: discord.Role):
        cur = self._db.cursor()
        cur.execute("INSERT INTO mods VALUES (?,?)", (role.id, role.guild.id))
        self._db.commit()
        print(f"database: added \"{role.name}\" from guild \"{role.guild.name}\" as a mod role")

    def remove(self, role: discord.Role):
        cur = self._db.cursor()
        cur.execute("DELETE FROM mods WHERE role_id = ? AND guild_id = ?", (role.id, role.guild.id))
        self._db.commit()
        print(f"database: removed mod role \"{role.name}\" from guild \"{role.guild.name}\"")

    def has(self, role: discord.Role):
        cur = self._db.cursor()
        cur.execute("SELECT COUNT(*) FROM mods WHERE role_id = ?", (role.id,))
        return cur.fetchone()[0] > 0

    def get_all(self, guild: discord.Guild):
        print(f"database: fetching mod roles for {guild.name}")
        cur = self._db.cursor()
        try:
            cur.execute("SELECT role_id FROM mods WHERE guild_id = ?", (guild.id,))
            return [r[0] for r in cur.fetchall()]
        except Exception as e:
            print(f"database: WARN error in mods.get_all: {e}")
            return []

    def clear(self, guild: discord.Guild):
        cur = self._db.cursor()
        cur.execute("DELETE FROM mods WHERE guild_id = ?", (guild.id,))
        self._db.commit()
        print(f"database: removed all mod roles from guild \"{guild.name}\"")
