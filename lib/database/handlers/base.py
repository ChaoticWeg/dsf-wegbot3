from abc import ABC, abstractmethod
from pathlib import Path

import sqlite3


class DatabaseHandler(ABC):
    def __init__(self, db_file: Path):
        self.db_file: Path = db_file
        self.db: sqlite3.Connection = sqlite3.connect(str(self.db_file))

    def initialize(self):
        """ Initialize the database handler using the subclass' implemented on_initialize """
        print(f"database: initializing {self.__class__.__name__}")
        self.on_initialize()

    def close(self):
        """ Close the database connection """
        print(f"database: closing {self.__class__.__name__}")
        self.db.close()

    @abstractmethod
    def on_initialize(self):
        """ Initialization logic for ensuring the proper table(s) exist with the proper schema(s) """
        pass
