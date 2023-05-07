import os


class Scan_DB_files:
    def __init__(self, dir_input):
        self.dir_input = dir_input

    def scan_db(self):
        danh_sach_db = []
        for root, dirs, files in os.walk(self.dir_input):
            for file in files:
                if file.endswith('.db'):
                    danh_sach_db.append(os.path.join(root, file))
        return danh_sach_db
