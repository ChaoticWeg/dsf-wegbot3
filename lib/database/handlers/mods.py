from pathlib import Path

import discord

from .base import DatabaseHandler


class ModsHandler(DatabaseHandler):
    def __init__(self, db_file: Path):
        super().__init__(db_file, "mods",
                         "guild_id TEXT NOT NULL, user_id TEXT NOT NULL, UNIQUE(guild_id, user_id)")

    @staticmethod
    def tuple_from_member(member: discord.Member):
        guild_id: str = str(member.guild.id)
        user_id: str = str(member.id)
        return guild_id, user_id

    def is_mod(self, member: discord.Member):
        print(f"database: {member.guild.name} :: checking mod status for {member}")

        cur = self.db.cursor()
        member_as_tuple: tuple = ModsHandler.tuple_from_member(member)

        cur.execute("SELECT COUNT(*) FROM mods WHERE guild_id = ? AND user_id = ?",
                    member_as_tuple)

        fetched: list = cur.fetchone()
        return fetched is not None and len(fetched) > 0 and fetched[0] > 0

    def add(self, member: discord.Member):
        if self.is_mod(member):
            print(f"database: {member.guild.name} :: tried adding {member} to mods, but member is already mod")
            return

        member_as_tuple: tuple = ModsHandler.tuple_from_member(member)

        print(f"database: {member.guild.name} :: adding {member} to mods")
        self.db.execute("INSERT INTO mods (guild_id, user_id) VALUES (?, ?)",
                        member_as_tuple)

        self.db.commit()
        print(f"database: {member.guild.name} :: successfully added {member} to mods")

    def remove(self, member: discord.Member):
        if not self.is_mod(member):
            print(f"database: {member.guild.name} :: tried removing {member} from mods, but member is not a mod")
            return

        member_as_tuple: tuple = ModsHandler.tuple_from_member(member)

        print(f"database: {member.guild.name} :: removing {member} from mods")
        self.db.execute("DELETE FROM mods WHERE guild_id = ? AND user_id = ?",
                        member_as_tuple)
        self.db.commit()
        print(f"database: {member.guild.name} :: successfully removed {member} from mods")
