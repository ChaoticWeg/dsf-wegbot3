from abc import ABC, abstractmethod
from pathlib import Path

import sqlite3


class DatabaseHandler(ABC):
    def __init__(self, dbfs_root: Path, dbname: str):
        self._dbfs_root = dbfs_root
        self._dbname = dbname
        self._db_filename = dbfs_root / f"{dbname}.db"
        self._db = sqlite3.connect(str(self._db_filename.resolve()))

    def initialize(self):
        print(f"database: initializing {self._dbname} handler")
        self.on_initialize()

    def close(self):
        print(f"database: closing connection for {self._dbname} handler")
        self._db.close()

    @abstractmethod
    def on_initialize(self):
        pass
