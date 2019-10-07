from pathlib import Path
from .base import DatabaseHandler

import discord


class RolesHandler(DatabaseHandler):
    def __init__(self, db_file: Path):
        super().__init__(db_file, "roles", "role_id TEXT NOT NULL UNIQUE, guild_id TEXT NOT NULL")

    def get_all(self, guild: discord.Guild):
        cur = self.db.cursor()
        cur.execute("SELECT role_id FROM roles WHERE guild_id = ?", (str(guild.id),))
        role_ids = [c[0] for c in cur.fetchall()]
        return [
            rnn for rnn in
            [discord.utils.find(lambda rr: str(rr.id) == rid, guild.roles) for rid in role_ids]
            if rnn is not None
        ]

    def put(self, role: discord.Role):
        self.db.execute("INSERT INTO roles (role_id, guild_id) VALUES (?,?)", (str(role.id), str(role.guild.id)))
        self.db.commit()

    def remove(self, role: discord.Role):
        self.db.execute("DELETE FROM roles WHERE role_id = ?", (str(role.id),))
        self.db.commit()

    def clear(self, guild: discord.Guild):
        self.db.execute("DELETE FROM roles WHERE guild_id = ?", (str(guild.id),))
        self.db.commit()

    def count(self, guild: discord.Guild):
        cur = self.db.cursor()
        cur.execute("SELECT COUNT(role_id) FROM roles WHERE guild_id = ?", (str(guild.id),))
        return cur.fetchone()[0]
