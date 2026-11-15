import sqlite3
import time
import sys


class SqliteDB:
    def __init__(self, filename):
        init(autoreset=True)
        self.filename = filename
        self.all_tables = None

    def isSQLite3(self):
        """
        Check if the database is sqlite or not:
        """
        from os.path import isfile, getsize

        if not isfile(self.filename):
            return False
        if getsize(self.filename) < 100:  # SQLite DB file header is 100 bytes
            return False

        with open(self.filename, 'rb') as fd:
            header = fd.read(100)

        return header[:16] == b'SQLite format 3\x00'

    def open(self):
        if not self.isSQLite3():
            raise sqlite3.DatabaseError("Not an SQLite DB")

        self.conn = sqlite3.connect(f"file:{self.filename}", uri=True)
        self.test()

    def test(self):
        c = self.conn.cursor()
        c.execute("select name from sqlite_master where type='table'")
        result = c.fetchall()
        c.close()
        return result
