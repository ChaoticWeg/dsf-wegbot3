import sqlite3
from pathlib import Path
from discord import Member

from .handlers import RolesHandler, KeyValueHandler, AdminChannelHandler, PermissionRequestsHandler, ModsHandler
from .paths import get_data_dir


class WegbotDatabase:
    def __init__(self):
        self.root: Path = get_data_dir()
        self.file: Path = self.root / "wegbot.db"

        self.__cnx: sqlite3.Connection = sqlite3.connect(str(self.file))
        self.__initialized: bool = False

        self.roles = RolesHandler(self.file)
        self.key_value = KeyValueHandler(self.file)
        self.admin_channel = AdminChannelHandler(self.file)
        self.mods = ModsHandler(self.file)
        self.permission_requests = PermissionRequestsHandler(self.file)

    def initialize(self):
        if self.__initialized:
            return

        self.roles.initialize()
        self.key_value.initialize()
        self.admin_channel.initialize()
        self.mods.initialize()
        self.permission_requests.initialize()

        self.__initialized = True

    def connect(self):
        return sqlite3.connect(str(self.file))

    def check_table(self, tablename: str):
        try:
            self.__cnx.execute(f"SELECT 1 FROM {tablename} LIMIT 1")
            return True
        except sqlite3.OperationalError:
            return False

    def check_mod(self, member: Member):
        try:
            return self.mods.is_mod(member)
        except sqlite3.OperationalError:
            return False
