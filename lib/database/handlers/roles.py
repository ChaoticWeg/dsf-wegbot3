from pathlib import Path
from .base import DatabaseHandler


class RolesHandler(DatabaseHandler):
    def __init__(self, db_file: Path):
        super().__init__(db_file, "roles", "role_id TEXT NOT NULL UNIQUE, guild_id TEXT NOT NULL")
