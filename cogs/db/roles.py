from pathlib import Path
from .handler import DatabaseHandler

import discord
import sqlite3


class RolesHandler(DatabaseHandler):
    def __init__(self, dbfs_root: Path):
        super().__init__(dbfs_root, "roles")

    def on_initialize(self):
        cur = self._db.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM roles")
            count = cur.fetchone()[0]
            print(f"database: {count} known requestable roles")
        except sqlite3.OperationalError:
            cur.execute("CREATE TABLE roles (id text NOT NULL UNIQUE, guild_id text NOT NULL)")
            self._db.commit()
            print(f"database: created new roles table")

    def add(self, role: discord.Role):
        cur = self._db.cursor()
        cur.execute("INSERT INTO roles VALUES (?,?)", (role.id, role.guild.id))
        self._db.commit()
        print(f"database: added \"{role.name}\" from guild \"{role.guild.name}\" as a requestable role")

    def remove(self, role: discord.Role):
        cur = self._db.cursor()
        cur.execute("DELETE FROM roles WHERE id = ? AND guild_id = ?", (role.id, role.guild.id))
        self._db.commit()
        print(f"database: removing requestable role '{role.name}' in guild '{role.guild.name}'")

    def has(self, role: discord.Role):
        cur = self._db.cursor()
        cur.execute("SELECT COUNT(*) FROM roles WHERE id = ? AND guild_id = ?", (role.id, role.guild.id))
        result = cur.fetchone()[0] > 0
        print(result)
        print(f"database: determining status of role {role.name} ({result})")
        return result

    def get_all(self, guild: discord.Guild):
        cur = self._db.cursor()
        cur.execute("SELECT id FROM roles WHERE guild_id = ?", (guild.id,))
        result = [r[0] for r in cur.fetchall()]
        result = [] if len(result) < 1 else result
        print(f"database: requestable roles for {guild.name} ({len(result)}): [{', '.join(result)}]")
        return result

    def clear(self, guild: discord.Guild):
        cur = self._db.cursor()
        cur.execute("DELETE FROM roles WHERE guild_id = ?", (guild.id,))
        self._db.commit()
        print(f"database: cleared roles for {guild.id}")
