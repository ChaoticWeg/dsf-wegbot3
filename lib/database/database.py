import sqlite3
from pathlib import Path

from .paths import get_data_dir
from .handlers import RolesHandler


class WegbotDatabase:
    def __init__(self):
        self.root: Path = get_data_dir()
        self.file: Path = self.root / "wegbot.db"
        self.__cnx: sqlite3.Connection = sqlite3.connect(str(self.file))

        self.roles = RolesHandler(self.file)

    def initialize(self):
        self.roles.initialize()

    def connect(self):
        return sqlite3.connect(str(self.file))

    def check_table(self, tablename: str):
        try:
            self.__cnx.execute(f"SELECT 1 FROM {tablename} LIMIT 1")
            return True
        except sqlite3.OperationalError:
            return False
