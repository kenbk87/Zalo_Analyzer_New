from Connect_DB import *
import pandas as pd
import numpy as np


class Get_Data_iOS:
    def __init__(self, df_danh_ba, duong_dan_zalo_file, duong_dan_zalo_group):
        self.df_danh_ba = df_danh_ba
        self.duong_dan_zalo_file = duong_dan_zalo_file
        self.duong_dan_zalo_group = duong_dan_zalo_group

    def get_data(self):
        query1 = 'SELECT fuid, tuid, message, datetime(ROUND(ts/1000), \'unixepoch\', \'localtime\'),' \
                 'metadata  from ChatEntity'
        df_final_1 = self.get_data_from(self.df_danh_ba, self.duong_dan_zalo_file, query1)

        query2 = 'SELECT fuid, tuid, message, datetime(ROUND(ts/1000), \'unixepoch\', \'localtime\'),' \
                 'metadata  from ChatGroupEntity'
        df_final_2 = self.get_data_from(self.df_danh_ba, self.duong_dan_zalo_group, query2)

        df_final_1 = pd.concat([df_final_1, df_final_2], ignore_index=True)
        df_final_1.index = np.arange(1, len(df_final_1) + 1)

        return df_final_1

    @staticmethod
    def get_data_from(danh_ba, duong_dan_file, query):
        """
        :param df_danh_ba:
        :param duong_dan_zalo_file:
        :return:
        """
        global df_merged_2
        df_danh_ba_tong_2 = danh_ba.rename(columns={'SenderId': 'AttendId', 'SenderName': 'AttendName'})

        try:
            du_lieu = Connect_DB(duong_dan_file, query).connect()
        except Exception as e:
            print(e)

        df_du_lieu = pd.DataFrame(du_lieu, columns=['SenderId', 'AttendId', 'Content', 'TimeStamp', 'Metadata'])

        # Left join với database danh bạ:
        try:
            df_du_lieu = df_du_lieu.astype({'SenderId': int}, errors='raise')
            df_merged_1 = pd.merge(df_du_lieu, danh_ba, how='left', on='SenderId')

            # Left join để ghép thêm cột AttendName:
            df_merged_1 = df_merged_1.astype({'AttendId': int}, errors='raise')
            df_merged_2 = pd.merge(df_merged_1, df_danh_ba_tong_2, how='left', on='AttendId')
        except Exception as e:
            print(e)

        # Đổi vị trí các cột:
        df_final = df_merged_2[
            ['SenderId', 'SenderName', 'AttendId', 'AttendName', 'TimeStamp', 'Content', 'Metadata']]

        # Thiết lập index bắt đầu từ 1, ép kiểu dữ liệu các cột sang string:
        df_final = df_final.astype({'Content': str}, errors='raise')
        df_final = df_final.astype({'SenderId': str}, errors='raise')
        df_final = df_final.astype({'AttendId': str}, errors='raise')
        df_final = df_final.astype({'SenderName': str}, errors='raise')
        df_final = df_final.rename(columns={'SenderId': 'ID người gửi',
                                            'SenderName': 'Tên người gửi',
                                            'AttendId': 'ID người nhận',
                                            'AttendName': 'Tên người nhận',
                                            'TimeStamp': 'Thời gian',
                                            'Content': 'Nội dung',
                                            'Metadata': 'Metadata'})
        return df_final

    def get_owner_name(self):
        """
            Lấy tên chủ tài khoản Zalo
        """
        query = 'SELECT userid from ChatEntity LIMIT 1'
        du_lieu = Connect_DB(self.duong_dan_zalo_file, query).connect()

        df_du_lieu = pd.DataFrame(du_lieu, columns=['SenderId'])
        df_du_lieu = df_du_lieu.astype({'SenderId': int}, errors='raise')

        df_merged_owner = pd.merge(df_du_lieu, self.df_danh_ba, how='left', on='SenderId')
        return df_merged_owner.iat[0, 1]

    def get_owner_id(self):
        """
            Lấy id chủ tài khoản Zalo
        """
        query = 'SELECT userid from ChatEntity LIMIT 1'
        du_lieu = Connect_DB(self.duong_dan_zalo_file, query).connect()
        return du_lieu[0][0]
