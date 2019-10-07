import sqlite3
from pathlib import Path


class DatabaseHandler:
    def __init__(self, db_file: Path, tablename: str, tableschema: str):
        self.db_file: Path = db_file
        self.db: sqlite3.Connection = sqlite3.connect(str(self.db_file))
        self.tablename = tablename
        self.tableschema = tableschema

    def initialize(self):
        """ Initialize the database handler """
        print(f"database: initializing {self.__class__.__name__}")
        self.on_preinitialize()

        self.db.execute(f"CREATE TABLE IF NOT EXISTS {self.tablename} ({self.tableschema})")
        self.db.commit()

        self.on_postinitialize()

    def close(self):
        """ Close the database connection """
        print(f"database: closing {self.__class__.__name__}")
        self.db.close()

    def on_preinitialize(self):
        pass

    def on_postinitialize(self):
        cur = self.db.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {self.tablename}")
        count = cur.fetchone()[0]
        print(f"database: {count} rows in table '{self.tablename}'")
        pass
