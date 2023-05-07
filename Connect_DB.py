import sqlite3
import os


class Connect_DB:
    def __init__(self, db_name, query):
        self.db_name = db_name
        self.query = query

    def connect(self):
        try:
            db = self.db_name.split('\\')[-1]
            print(f'Đang kết nối đến database: {db}')

            # Mở file database ở chế độ chỉ đọc để không làm ảnh hưởng đến file wal và file shm:
            sqlite_connect = sqlite3.connect(f"file:{self.db_name}?mode=ro", uri=True)
            cursor = sqlite_connect.cursor()
            cursor.execute(self.query)
            result = cursor.fetchall()
            cursor.close()
            return result

        except sqlite3.Error as error:
            print('Error occurred', error)
        finally:
            if sqlite_connect:
                sqlite_connect.close()

