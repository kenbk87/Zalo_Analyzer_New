import pandas as pd
import numpy as np
from Connect_DB import *

class ExtractZaloDB:
    def __init__(self, df_contact, danh_sach_db):
        self.df_contact = df_contact
        self.danh_sach_db = danh_sach_db
        # Trích xuất dữ liệu tin nhắn từ thư mục database:

    def extract_data(self):
        df = pd.DataFrame(columns=['SenderId', 'TimeStamp', 'Content', 'LocalPath'])
        df_danh_ba_tong_2 = self.df_contact.rename(columns={'SenderId': 'AttendId', 'SenderName': 'AttendName'})
        so_db = len(self.danh_sach_db)

        for i in range(so_db):
            substring = 'group_'
            query4 = 'SELECT SenderId, datetime(ROUND(TimeStamp/1000), \'unixepoch\', \'localtime\'), MsgContent, ' \
                     'LocalPath, BinNet from ChatContent'

            # Lấy dữ liệu tin nhắn từ từng database:
            dulieu = Connect_DB(self.danh_sach_db[i], query4).connect()

            ten_db = self.danh_sach_db[i]
            # Tách riêng phần ID có trong tên file:
            # Loại bỏ chữ 'group_', chỉ lấy ID của nhóm:
            if substring in ten_db:
                ten_db = ten_db.split(substring)[1]
                ten_db = ten_db.split('.')[0]
            else:
                ten_db = ten_db.split('\\')[-1]
                ten_db = ten_db.split('.')[0]

            df_new = pd.DataFrame(dulieu, columns=['SenderId', 'TimeStamp', 'Content', 'LocalPath', 'BinNet'])
            df_new.insert(5, 'AttendId', ten_db)

            df = pd.concat([df, df_new], ignore_index=True)

        # Left join với database danh bạ:
        df_merged_1 = pd.merge(df, self.df_contact, how='left', on='SenderId')
        df_merged_1 = df_merged_1.astype({'AttendId': int}, errors='raise')

        # Left join để ghép thêm cột AttendName:
        df_merged_2 = pd.merge(df_merged_1, df_danh_ba_tong_2, how='left', on='AttendId')

        # Đổi vị trí các cột:
        df_final = df_merged_2[
            ['SenderId', 'SenderName', 'AttendId', 'AttendName', 'TimeStamp', 'Content', 'LocalPath', 'BinNet']]

        # Thiết lập index bắt đầu từ 1, ép kiểu dữ liệu các cột sang string:
        df_final.index = np.arange(1, len(df_final) + 1)
        df_final = df_final.astype({'Content': str}, errors='raise')
        df_final = df_final.astype({'SenderId': str}, errors='raise')
        df_final = df_final.astype({'AttendId': str}, errors='raise')
        df_final = df_final.astype({'SenderName': str}, errors='raise')

        return df_final



