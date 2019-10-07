from pathlib import Path
from .paths import get_data_dir

import sqlite3


class WegbotDatabase:
    def __init__(self):
        self.root: Path = get_data_dir()
        self.file: Path = self.root / "wegbot.db"

    def connect(self):
        return sqlite3.connect(str(self.file))
