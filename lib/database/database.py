import sqlite3
from pathlib import Path

from .paths import get_data_dir
from .handlers import RolesHandler, KeyValueHandler


class WegbotDatabase:
    def __init__(self):
        self.root: Path = get_data_dir()
        self.file: Path = self.root / "wegbot.db"

        self.__cnx: sqlite3.Connection = sqlite3.connect(str(self.file))
        self.__initialized: bool = False

        self.roles = RolesHandler(self.file)
        self.key_value = KeyValueHandler(self.file)

    def initialize(self):
        if self.__initialized:
            return

        self.roles.initialize()
        self.key_value.initialize()

        self.__initialized = True

    def connect(self):
        return sqlite3.connect(str(self.file))

    def check_table(self, tablename: str):
        try:
            self.__cnx.execute(f"SELECT 1 FROM {tablename} LIMIT 1")
            return True
        except sqlite3.OperationalError:
            return False
