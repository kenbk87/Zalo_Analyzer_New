import tarfile
import tkinter as tk
import zipfile
from tkinter import filedialog as fd
from tkinter import messagebox as ms
from tkinter import ttk
from tkinter import scrolledtext
from tktooltip import ToolTip
from zipfile import ZipFile

from pandastable import Table

from Path_Zalo_iOS import Zalo_iOS
from Extract_Zalo_iOS import Analysis_Zalo_iOS
from Extract_From_ZaloDB import *
from Scan_DB_Files import Scan_DB_files
import webbrowser

from threading import Thread
import pandas as pd
import os


class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Zalo Analyzer 2.0 - Designed by K3n')
        # self.iconbitmap('./Resource/image/trash.png')
        # Call style:
        self.style = ttk.Style(self)
        self.tk.call('source', 'forest-light.tcl')
        self.tk.call('source', 'forest-dark.tcl')
        self.style.theme_use('forest-dark')

        # Create self frame that contain all frame:
        frame = ttk.Frame(self)
        frame.pack()

        ################################################################################################################
        # Create the first frame:
        self.widgets_frame = ttk.LabelFrame(frame, text='Image file analysis: ')
        self.widgets_frame.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky='nsew')

        self.entry_file_selected = ttk.Entry(self.widgets_frame, width=55)
        self.entry_file_selected.insert(0, 'Select image file')
        self.entry_file_selected.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.entry_folder_selected = ttk.Entry(self.widgets_frame)
        self.entry_folder_selected.insert(0, 'Select save folder')
        self.entry_folder_selected.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.button_select_file = ttk.Button(self.widgets_frame, text='Browse', command=self.select_file)
        self.button_select_file.grid(row=0, column=1, padx=5, pady=5)

        self.button_select_folder = ttk.Button(self.widgets_frame, text='Browse', command=self.select_folder)
        self.button_select_folder.grid(row=1, column=1, padx=5, pady=5)

        self.separator = ttk.Separator(self.widgets_frame, orient='vertical')
        self.separator.grid(row=0, column=2, rowspan=2, padx=5, pady=5, sticky='ns')

        self.button_unzip = ttk.Button(self.widgets_frame, text='Analysis', command=self.unzip_threading, width=18)
        self.button_unzip.grid(row=0, column=3, columnspan=2, padx=5, pady=10, sticky='nsew')

        self.mode_switch = ttk.Checkbutton(self.widgets_frame, text='Mode', style='Switch', command=self.toggle_mode)
        self.mode_switch.grid(row=1, column=4, padx=5, pady=5, sticky='ew')

        ################################################################################################################
        # Create the second frame:
        self.folder_frame = ttk.LabelFrame(frame, text='Image folder analysis:')
        self.folder_frame.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        self.entry_folder_selected_2 = ttk.Entry(self.folder_frame, width=40)
        self.entry_folder_selected_2.insert(0, 'Select image folder')
        self.entry_folder_selected_2.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.button_select_folder_2 = ttk.Button(self.folder_frame, text='Browse', command=self.select_folder_image)
        self.button_select_folder_2.grid(row=0, column=1, padx=5, pady=10)

        self.separator = ttk.Separator(self.folder_frame, orient='vertical')
        self.separator.grid(row=0, column=2, padx=5, pady=5, sticky='ns')

        self.button_folder_analysis = ttk.Button(self.folder_frame, text='Analysis', command=self.scan_folder_threading,
                                                 width=18)
        self.button_folder_analysis.grid(row=0, column=3, columnspan=2, padx=5, pady=5, sticky='ew')

        ################################################################################################################
        # Create a third frame:
        self.info_frame = ttk.LabelFrame(frame, text='Account info:')
        self.info_frame.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

        self.info_1 = ttk.Label(self.info_frame, text='Number of conversation: ')
        self.info_1.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.number_conversation = ttk.Label(self.info_frame, text='                        ')
        self.number_conversation.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.info_2 = ttk.Label(self.info_frame, text='Zalo Owner ID: ')
        self.info_2.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.zalo_owner_id = ttk.Label(self.info_frame, text='                        ')
        self.zalo_owner_id.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.info_3 = ttk.Label(self.info_frame, text='Zalo Owner Name: ')
        self.info_3.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        self.zalo_owner_name = ttk.Label(self.info_frame, text='                        ')
        self.zalo_owner_name.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        ################################################################################################################
        # Create a frame to display data:
        self.result_frame = ttk.LabelFrame(frame, text='Result:')
        self.result_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='news')

        self.pt = Table(self.result_frame, showtoolbar=True, showstatusbar=True)
        self.pt.show()

        ################################################################################################################
        # Create a status frame:
        self.status_frame = ttk.LabelFrame(frame, text='Status:')
        self.status_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='ew')

        self.lb_status = ttk.Label(self.status_frame)
        self.lb_status.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.progress_bar = ttk.Progressbar(self.status_frame, length=1100)
        self.progress_bar.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        ################################################################################################################
        # Create a export frame:
        self.export_frame = ttk.LabelFrame(frame, text='Export:')
        self.export_frame.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

        global var
        var = tk.IntVar()
        self.radiobutton_excel = ttk.Radiobutton(self.export_frame, text='Excel', variable=var, value=0)
        self.radiobutton_excel.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.radiobutton_html = ttk.Radiobutton(self.export_frame, text='HTML', variable=var, value=1)
        self.radiobutton_html.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.radiobutton_csv = ttk.Radiobutton(self.export_frame, text='CSV', variable=var, value=2)
        self.radiobutton_csv.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        self.btn_export = ttk.Button(self.export_frame, text='Export', command=self.trich_xuat)
        self.btn_export.grid(row=0, column=3, pady=5, padx=50, columnspan=3, sticky='ew')

        self.btn_view = ttk.Button(self.export_frame, text='Open', command=self.xem)
        self.btn_view.grid(row=1, column=3, pady=5, padx=50, columnspan=3, sticky='ew')
        ################################################################################################################
        # Create a log frame:
        self.log_frame = ttk.LabelFrame(frame, text='Log:')
        self.log_frame.grid(row=2, column=2, padx=5, pady=5, sticky='nsew')

        self.entry_log = scrolledtext.ScrolledText(self.log_frame, height=6)
        self.entry_log.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        ################################################################################################################
        # Create a tooltip:
        ToolTip(self.button_unzip, 'With an image file: \n'
                                   '1. Select image zip file \n'
                                   '2. Select folder to save after unzip \n'
                                   '3. Click this button to analysis')

        ToolTip(self.button_folder_analysis, 'With a folder contain file after unzip: \n'
                                             '1. Select folder \n'
                                             '2. Click this button to analysis')

    def toggle_mode(self):
        """
            Switch display mode
        """
        if self.mode_switch.instate(['selected']):
            self.style.theme_use('forest-light')
        else:
            self.style.theme_use('forest-dark')

    def select_file(self):
        """
            Select image file to extract:
        """
        file_name = fd.askopenfilename()
        self.entry_file_selected.delete('0', 'end')
        self.entry_file_selected.insert(0, file_name)

    def select_folder(self):
        """
            Select folder to save unzip file
        """
        folder = fd.askdirectory()
        self.entry_folder_selected.delete('0', 'end')
        self.entry_folder_selected.insert(0, folder)

    def select_folder_image(self):
        """
            Select image folder to analysis
        """
        folder = fd.askdirectory()
        self.entry_folder_selected_2.delete('0', 'end')
        self.entry_folder_selected_2.insert(0, folder)

    def unzip_threading(self):
        """
            Create another thread to prevent freeze GUI
        """
        thread_1 = Thread(target=self.load_data)
        thread_1.start()

    def scan_folder_threading(self):
        """
            Create another thread to prevent freeze GUI
        """
        thread_2 = Thread(target=self.scan_image_folder)
        thread_2.start()

    def unzip(self):
        """
            1. Unzip a zip file with zipfile library
            2. Unzip a tar file with
        """
        file_name = self.entry_file_selected.get().strip()
        file_name = '\\\\?\\' + file_name.replace('/', '\\')
        save_folder = self.entry_folder_selected.get().strip()
        save_folder = '\\\\?\\' + save_folder.replace('/', '\\')
        self.entry_log.insert(tk.END, f'- Đã chọn thư mục lưu: {save_folder} \n')
        if file_name.endswith('.zip'):
            with ZipFile(file_name) as zip_file:
                file_list = zip_file.namelist()
                try:
                    for idx, files in enumerate(file_list, 1):
                        percent = round((idx / len(file_list)) * 100, 2)
                        self.lb_status.config(text=f'{percent}%')
                        self.progress_bar['value'] = percent
                        zip_file.extract(files, save_folder)
                        self.entry_log.insert(tk.END, f'- Extracting: {os.path.basename(files)}...\n')
                except zipfile.BadZipfile as e:
                    self.entry_log.insert(tk.END, f'- {e} \n')
            zip_file.close()

        elif tarfile.is_tarfile(file_name):
            self.entry_log.insert(tk.END, f'- Đã chọn file ảnh định dạng tar file: {os.path.basename(file_name)}\n')
            with tarfile.open(file_name) as Tar_file:
                file_list = Tar_file.getmembers()
                for idx, files in enumerate(file_list, 1):
                    percent = round((idx / len(file_list)) * 100, 2)
                    self.lb_status.config(text=f'{percent}%')
                    self.progress_bar['value'] = percent
                    try:
                        Tar_file.extract(files, save_folder)
                    except Exception as e:
                        self.entry_log.insert(tk.END, f'- {e} \n')
            Tar_file.close()
        self.entry_log.insert(tk.INSERT, f'- Extract {os.path.basename(file_name)} done!!! \n')
        self.entry_log.see(tk.END)

    def display_data(self, df):
        self.pt.model.df = df
        self.pt.editable = False
        self.pt.font = 'Arial'
        self.pt.fontsize = 5
        self.pt.redraw()
        self.pt.show()

    def load_data(self):
        """
            1. Unzip image file
            2. Scan extracted folder and display result
        """
        folder_name = self.entry_folder_selected.get().strip()
        if folder_name == '' or folder_name == 'Select save folder':
            ms.showwarning('Wanring', 'Please select folder to save!!')
        else:
            self.unzip()
            self.scan_folder(folder_name)

    def scan_image_folder(self):
        folder_name = self.entry_folder_selected_2.get().strip()
        if folder_name == '' or folder_name == 'Select image folder':
            ms.showwarning('Wanring', 'Please select folder to scan!!')
        else:
            self.scan_folder(folder_name)

    def scan_folder(self, folder_selected):
        global df_danh_ba_tong
        if folder_selected == '':
            ms.showwarning('Warning', 'Chưa chọn thư mục để lưu \U0001F606 \U0001F606 \U0001F606')
        else:
            duong_dan = ''
            # Chia làm 2 lần quét, quét thư mục com.zing.zalo trước
            for root, dirs, files in os.walk(folder_selected):
                ZALO_DIR = 'data\data\com.zing.zalo'
                DIR_iOS = 'private\\var\mobile\Library\FrontBoard'
                for dir in dirs:
                    dd = os.path.join(root, dir)
                    if dd.endswith(ZALO_DIR):
                        duong_dan = dd
                        operating_system = 'android'
                        self.entry_log.insert(tk.END, f'- Đã tìm thấy dữ liệu ứng dụng Zalo \n')
                        break
                    elif dd.endswith(DIR_iOS):
                        operating_system = 'iOS'
                        duong_dan = dd
                        break
            if duong_dan == '':
                ms.showwarning('Warning', 'Không tìm thấy dữ liệu ứng dụng Zalo \U0001F605 \U0001F605 \U0001F605')

            self.entry_log.insert(tk.END, f'- Điện thoại sử dụng hệ điều hành {operating_system} \n')

            if operating_system == 'android':
                self.entry_log.insert(tk.END, f'- Đường dẫn zalo: {duong_dan} \n')
                self.db_analysic(duong_dan)
            elif operating_system == 'iOS':
                global df_final_1
                # Cắt lấy phần đầu của biến duong_dan:
                dd1 = duong_dan.split('\\private')[0]
                zalo_path = Zalo_iOS(duong_dan).scan_zalo_iOS()

                # Đường dẫn đầy đủ chứa dữ liệu của Zalo:
                path_full = dd1 + zalo_path
                db_path = Analysis_Zalo_iOS(path_full).find_db()

                try:
                    list_db = Scan_DB_files(db_path).scan_db()

                    df_danh_ba_tong = Analysis_Zalo_iOS(path_full).analysis()
                    df = ExtractZaloDB(df_danh_ba_tong, list_db).extract_data()

                    id_zalo_owner = self.get_zalo_owner_iOS(db_path, df_danh_ba_tong)
                    df_final_1 = self.replace_receiver(df, id_zalo_owner)

                    self.display_data(df_final_1)
                except Exception as e:
                    print(e)

    def db_analysic(self, zalo_path):
        global df_final_1, df_final_2
        ZALO = 'zalo'
        FILE_BIN_1 = 'phone_contact_list_server_version.bin'
        FILE_BIN_2 = 'phonecontactlist.bin'

        # Tạo mảng danh_sach_bin_file chứa đường dẫn của 02 file .bin
        # Tạo mảng danh_ba chứa đường dẫn của file 'zalo'
        global danh_ba
        danh_sach_bin_file, danh_ba = [], []

        # Quét tất cả các file, thư mục có trong đường dẫn đã chọn:
        for root, dirs, files in os.walk(zalo_path):
            for name in files:
                file = os.path.join(root, name)
                if FILE_BIN_1 in file:
                    danh_sach_bin_file.append(file)
                elif FILE_BIN_2 in file:
                    danh_sach_bin_file.append(file)
                elif name == ZALO:
                    danh_ba.append(file)

        # Lấy số tài khoản Zalo:
        # Nếu số tài khoản zalo = 0 mà vẫn tồn tại thư mục com.zing.zalo thì ta vẫn có thể lấy dữ liệu tin nhắn:

        contact_zalo = self.get_contact(danh_ba[0], danh_sach_bin_file)
        number_of_zalo = self.get_zalo_owner_info(zalo_path)

        if number_of_zalo == 1:
            db_list_1 = Scan_DB_files(owner_id_path[0]).scan_db()
            so_db = len(db_list_1)

            df_final_1 = self.get_data(contact_zalo, db_list_1)
            df_final_1 = self.replace_receiver(df_final_1, owner_id[0])

        elif number_of_zalo == 2:
            db_list_1 = Scan_DB_files(owner_id_path[0]).scan_db()
            db_list_2 = Scan_DB_files(owner_id_path[1]).scan_db()
            so_db = len(db_list_1) + len(db_list_2)

            df_final_1 = self.get_data(contact_zalo, db_list_1)
            df_final_1 = self.replace_receiver(df_final_1, owner_id[0])

            df_final_2 = self.get_data(contact_zalo, db_list_2)
            df_final_2 = self.replace_receiver(df_final_2, owner_id[0])

            df_final_1 = pd.concat([df_final_1, df_final_2], ignore_index=True)
            df_final_1.index = np.arange(1, len(df_final_1) + 1)

        elif number_of_zalo == 0:
            df_final_1 = self.get_data_no_db(contact_zalo, danh_ba[0])
            df_final_1.index = np.arange(1, len(df_final_1) + 1)
            so_db = 0

        try:
            self.display_data(df_final_1)
        except Exception as e:
            print(e)

        self.entry_log.insert(tk.END, f'- Đã quét xong {so_db} databases \n')
        self.number_conversation.config(text=f'{so_db}')

    def get_zalo_owner_iOS(self, duong_dan, df_contact):
        """
            Get information of Zalo owner on iOS
        """
        id_owner_zalo = duong_dan.split('\\')[-1]
        # Tìm tên chủ tài khoản Zalo:
        df_thong_tin_chu_tk = df_contact.loc[df_contact['SenderId'] == int(id_owner_zalo)]
        zalo_name_owner = df_thong_tin_chu_tk.iat[0, 1]
        self.zalo_owner_name.config(text=f'- Tài khoản: {zalo_name_owner}')
        self.zalo_owner_id.config(text=id_owner_zalo)
        return int(id_owner_zalo)

    def get_zalo_owner_info(self, duong_dan):
        """
            Get information of Zalo owner on Android
        """
        global owner_id, owner_id_path
        owner_id, owner_id_path = [], []
        TK_DATABASE = 'com.zing.zalo\\databases\\'
        for root, dirs, files in os.walk(duong_dan):
            for dir in dirs:
                dir_1 = os.path.join(root, dir)
                if TK_DATABASE in dir_1:
                    owner_id_path.append(dir_1)
                    owner_id.append(dir_1.split('\\')[-1])

        # Lấy id, tên chủ tài khoản Zalo:
        number_id = len(owner_id)

        self.entry_log.insert(tk.END, f'- Có {number_id} tài khoản Zalo \n')
        if number_id == 0:
            query = 'SELECT currentUserUid from chat_content LIMIT 1'
            du_lieu = Connect_DB(danh_ba[0], query).connect()

            owner_id.append(du_lieu[0][0])
            self.zalo_owner_id.config(text=f'{owner_id[0]}')

            # Tìm tên chủ tài khoản Zalo:
            df_thong_tin_chu_tk = df_danh_ba_tong[(df_danh_ba_tong['SenderId'] == int(owner_id[0]))]
            self.zalo_owner_name.config(text=f'- Tài khoản: {df_thong_tin_chu_tk.iat[0, 1]}')

        elif number_id == 1:
            self.zalo_owner_id.config(text=f'{owner_id[0]}')
        elif number_id == 2:
            self.zalo_owner_id.config(text=f'{owner_id[0]}, {owner_id[1]}')
        return number_id

    def get_contact(self, path_zalo_file, ds_bin_file):
        """
            Get contact data of Zalo
        """
        df_merged_3 = pd.DataFrame(columns=['dbId', 'zaloUid', 'displayName', 'numberInter', 'number'])

        # Lấy danh bạ từ 02 file .bin (phone_contact_list_server_version.bin, phonecontactlist.bin):
        for i in ds_bin_file:
            data_json = pd.read_json(i)
            df_merged_3 = pd.concat([df_merged_3, data_json], ignore_index=True)

        # Chỉ lấy 2 cột zaloUid và displayName:
        df_merged_3 = df_merged_3[['zaloUid', 'displayName']]
        df_merged_3 = df_merged_3.drop_duplicates(subset=['zaloUid', 'displayName'])
        # Phần này trở lên đã OK

        # Lấy danh bạ từ bảng contact_profile_5 trong database 'zalo':
        query1 = 'SELECT uid, dpn from contact_profile_5'
        du_lieu = Connect_DB(path_zalo_file, query1).connect()

        df_1 = pd.DataFrame(du_lieu, columns=['uid', 'dpn'])
        df_1 = df_1.rename(columns={'uid': 'zaloUid', 'dpn': 'displayName'})

        # Lấy danh bạ từ bảng chat_content trong database 'zalo':
        query2 = 'SELECT senderUid, senderName from chat_content'
        try:
            du_lieu_2 = Connect_DB(path_zalo_file, query2).connect()

            df_2 = pd.DataFrame(du_lieu_2, columns=['senderUid', 'senderName'])
            df_2 = df_2.rename(columns={'senderUid': 'zaloUid', 'senderName': 'displayName'})
            df_2 = df_2[df_2.zaloUid != 0]
        except Exception as e:
            print(e)
            df_2 = pd.DataFrame()

        # Lấy dữ liệu danh bạ từ bảng contact_profile_zalo trong database 'zalo':
        query3 = 'SELECT uid, dpn from contact_profile_zalo where uid not in (SELECT uid from contact_profile_5)'
        du_lieu_3 = Connect_DB(path_zalo_file, query3).connect()

        df_3 = pd.DataFrame(du_lieu_3, columns=['uid', 'dpn'])
        df_3 = df_3.rename(columns={'uid': 'zaloUid', 'dpn': 'displayName'})

        # Lấy dữ liệu danh bạ nhóm từ bảng group_info_v6 trong database 'zalo':
        query5 = 'SELECT id, name from group_info_v6'
        du_lieu_5 = Connect_DB(path_zalo_file, query5).connect()

        df_5 = pd.DataFrame(du_lieu_5, columns=['id', 'name'])
        df_5 = df_5.rename(columns={'id': 'zaloUid', 'name': 'displayName'})

        # Gộp lại với phần danh bạ lấy từ 02 file .bin:
        df_merged_3 = pd.concat([df_merged_3, df_1, df_2, df_3, df_5], ignore_index=True)

        # Đổi tên cột để left join theo SenderId:
        global df_danh_ba_tong
        df_danh_ba_tong = df_merged_3.rename(columns={'zaloUid': 'SenderId', 'displayName': 'SenderName'})
        try:
            # Xóa những dòng có giá trị NaN khi convert sang int sẽ bị lỗi:
            df_danh_ba_tong = df_danh_ba_tong.dropna()
            df_danh_ba_tong = df_danh_ba_tong.astype({'SenderId': int})
        except Exception as e:
            print(e)

        # Xóa những dòng trùng giá trị 'SenderId':
        df_danh_ba_tong = df_danh_ba_tong.drop_duplicates(subset=['SenderId'])
        return df_danh_ba_tong

    def get_data(self, df_danh_ba_tong, danh_sach_db):
        df = pd.DataFrame(columns=['SenderId', 'TimeStamp', 'Content', 'LocalPath'])
        df_danh_ba_tong_2 = df_danh_ba_tong.rename(columns={'SenderId': 'AttendId', 'SenderName': 'AttendName'})
        so_db = len(danh_sach_db)
        dem = 1

        for i in range(so_db):
            substring = 'group_'
            query4 = 'SELECT SenderId, datetime(ROUND(TimeStamp/1000), \'unixepoch\', \'localtime\'), MsgContent, ' \
                     'LocalPath, BinNet from ChatContent'

            # Lấy dữ liệu tin nhắn từ từng database:
            dulieu = Connect_DB(danh_sach_db[i], query4).connect()

            ten_db = danh_sach_db[i]
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
            dem += 1
            percent = round((dem / so_db) * 100, 2)
            self.lb_status.config(text=f'{percent}%')
            self.progress_bar['value'] = percent

        # Left join với database danh bạ:
        df_merged_1 = pd.merge(df, df_danh_ba_tong, how='left', on='SenderId')
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

        # Hàm lấy dữ liệu tin nhắn từ file zalo khi không có các database tin nhắn:

    def get_data_no_db(self, df_danh_ba, duong_dan_zalo_file):

        df_danh_ba_tong_2 = df_danh_ba.rename(columns={'SenderId': 'AttendId', 'SenderName': 'AttendName'})

        query = 'SELECT senderUid, message, ownerId, datetime(ROUND(timestamp/1000), \'unixepoch\', \'localtime\'),' \
                'localpath  from chat_content'
        du_lieu = Connect_DB(duong_dan_zalo_file, query).connect()

        df_du_lieu = pd.DataFrame(du_lieu, columns=['SenderId', 'Content', 'AttendId', 'TimeStamp', 'LocalPath'])

        # Left join với database danh bạ:
        try:
            df_du_lieu = df_du_lieu.astype({'SenderId': int}, errors='raise')
            df_merged_1 = pd.merge(df_du_lieu, df_danh_ba, how='left', on='SenderId')
            do_dai = len(df_merged_1)

            for i in range(do_dai):
                b = df_merged_1.iloc[i]['AttendId']
                if 'group' in b:
                    b1 = b.split('_')[1]
                    df_merged_1._set_value(i, 'AttendId', b1)

            # Thay thế người nhận khi trường người gửi và người nhận giống nhau:
            for i in range(do_dai):
                if int(df_merged_1.iloc[i]['SenderId']) == int(df_merged_1.iloc[i]['AttendId']):
                    df_merged_1._set_value(i, 'AttendId', owner_id[0])

            df_merged_1 = df_merged_1.astype({'AttendId': int}, errors='raise')

            # Left join để ghép thêm cột AttendName:
            df_merged_2 = pd.merge(df_merged_1, df_danh_ba_tong_2, how='left', on='AttendId')
        except Exception as e:
            print(e)

        # Đổi vị trí các cột:
        df_final = df_merged_2[
            ['SenderId', 'SenderName', 'AttendId', 'AttendName', 'TimeStamp', 'Content', 'LocalPath']]

        # Thiết lập index bắt đầu từ 1, ép kiểu dữ liệu các cột sang string:
        df_final = df_final.astype({'Content': str}, errors='raise')
        df_final = df_final.astype({'SenderId': str}, errors='raise')
        df_final = df_final.astype({'AttendId': str}, errors='raise')
        df_final = df_final.astype({'SenderName': str}, errors='raise')
        df_final = df_final.rename(columns={'SenderId': 'ID người gửi',
                                            'SenderName': 'Tên người gửi',
                                            'AttendId': 'ID hội thoại',
                                            'AttendName': 'Tên người nhận',
                                            'TimeStamp': 'Thời gian',
                                            'Content': 'Nội dung',
                                            'LocalPath': 'Đường dẫn',
                                            'BinNet': 'Byte data'})

        return df_final

        # Xử lý thông tin về người nhận tin nhắn:

    def replace_receiver(self, df, id_chu_tk):
        do_dai = len(df)
        df_thong_tin_chu_tk = df_danh_ba_tong[(df_danh_ba_tong['SenderId'] == int(id_chu_tk))]
        self.zalo_owner_name.config(text=f'- Tài khoản: {df_thong_tin_chu_tk.iat[0, 1]} có {do_dai} tin nhắn.')

        for i in range(do_dai):
            # byte_data = df.iloc[i]['BinNet']
            # data_decode = byte_data.decode('utf-8', 'ignore')
            #
            # df._set_value(i + 1, 'BinNet', data_decode)

            if df.iloc[i]['SenderId'] == df.iloc[i]['AttendId']:
                df._set_value(i + 1, 'AttendName', df_thong_tin_chu_tk.iat[0, 1])

        df = df.rename(columns={'SenderId': 'ID người gửi',
                                'SenderName': 'Tên người gửi',
                                'AttendId': 'ID hội thoại',
                                'AttendName': 'Tên người nhận',
                                'TimeStamp': 'Thời gian',
                                'Content': 'Nội dung',
                                'LocalPath': 'Đường dẫn',
                                'BinNet': 'Byte data'})
        return df

        # Trích xuất dữ liệu ra định dạng excel hoặc html:

    def trich_xuat(self):
        global ten_folder
        ten_folder = fd.askdirectory()
        self.entry_log.insert(tk.END, f'- Đã chọn thư mục: {ten_folder} \n')
        # Xử lý lỗi khi xuất ra file .csv không hiển thị được số 0 ở đầu số điện thoại
        df = df_final_1.copy()
        df['Nội dung'] = df['Nội dung'].apply('="{}"'.format)
        rd_button = var.get()

        if len(df.index) == 0:
            ms.showwarning('Warning', 'Chưa có dữ liệu để trích xuất')
        else:
            if rd_button == 2:
                df.to_csv(os.path.join(ten_folder, 'Zalo messages.csv'), encoding='utf-16', sep='\t', na_rep='N/A')
                self.entry_log.insert(tk.END, '- Đã trích xuất xong \n')
            elif rd_button == 1:
                df.to_html(os.path.join(ten_folder, 'Zalo messages.html'), justify='center', bold_rows=False)
                self.entry_log.insert(tk.END, '- Đã trích xuất xong \n')

    def xem(self):
        webbrowser.open(os.path.realpath(ten_folder))


if __name__ == '__main__':
    app = Window()
    # app.resizable(0, 0)
    app.mainloop()
