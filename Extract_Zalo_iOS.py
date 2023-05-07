import os
from Connect_DB import *
import pandas as pd


class Analysis_Zalo_iOS:
    def __init__(self, path):
        self.path = path

    # Trích xuất danh bạ từ thư mục ứng dụng Zalo:
    def analysis(self):
        path_contact = ''
        path_contact_2 = ''
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if str(file) == 'profile.sqlite':
                    path_contact = os.path.join(root, file)
                    break
                elif str(file) == 'chatgroup.sqlite':
                    path_contact_2 = os.path.join(root, file)
        if path_contact == '':
            print('Không tìm thấy dữ liệu danh bạ')

        query = 'SELECT zaloid, displayname from BuddyEntity where zaloid not in (select userid from ProfileEntity) ' \
                'union all select zaloid, displayname from ExtFriendRequestEntity  ' \
                'where zaloid not in (select userid from ProfileEntity) ' \
                'and zaloid not in (SELECT zaloid from BuddyEntity) ' \
                'union all select userid, displayname from ProfileEntity'

        query_2 = 'select groupid, name from GroupEntity'

        data = Connect_DB(path_contact, query).connect()
        df_contact_1 = pd.DataFrame(data, columns=['SenderId', 'SenderName'])

        data = Connect_DB(path_contact_2, query_2).connect()
        df_contact_2 = pd.DataFrame(data, columns=['SenderId', 'SenderName'])

        df_contact = pd.concat([df_contact_1, df_contact_2], ignore_index=True)
        df_contact = df_contact.astype({'SenderId': int})

        return df_contact

    # Tìm thư mục chứa database tin nhắn Zalo:
    def find_db(self):
        chat_folder = ''
        db_path = ''
        for root, dirs, files in os.walk(self.path):
            for dir_chat in dirs:
                if str(dir_chat) == 'chat_dbs':
                    chat_folder = os.path.join(root, dir_chat)

        for root, dirs, files in os.walk(chat_folder):
            for dir_1 in dirs:
                path_1 = os.path.join(root, dir_1)
                for root2, dirs2, files2 in os.walk(path_1):
                    for file_db in files2:
                        if file_db.endswith('.db'):
                            db_path = path_1
                            break
                        else:
                            print('Khong tim thay file .db')
        return db_path






