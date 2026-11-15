import sys
from Connect_DB import *
import os
import biplist
import io
import nska_deserialize as nd
import plistlib


class Zalo_iOS:
    def __init__(self, path):
        self.duong_dan = path

    def scan_zalo_iOS(self):
        for root, dirs, files in os.walk(self.duong_dan):
            for file in files:
                if str(file) == 'applicationState.db':
                    path_1 = os.path.join(root, file)
                    break

        query = 'SELECT id from application_identifier_tab where application_identifier = \'vn.com.vng.zingalo\''
        du_lieu = Connect_DB(path_1, query).connect()

        id_zalo = str(du_lieu[0][0])
        query_2 = f'SELECT value from kvs where application_identifier = {id_zalo} and key = 1'
        du_lieu_2 = Connect_DB(path_1, query_2).connect()

        # Giải mã dữ liệu Binary Plist từ trường Blob trong database applicationState.db:
        # Dữ liệu này có chứa đường dẫn đên database của ứng dụng Zalo:
        usageentries = len(du_lieu_2)

        if usageentries > 0:
            for row in du_lieu_2:
                bundleid = row[0]

                # BytesIO được sử dụng với dữ liệu binary:
                plist_file_object = io.BytesIO(bundleid)
                if bundleid.find(b'NSKeyedArchiver') == -1:
                    if sys.version_info >= (3, 9):
                        plist = plistlib.load(plist_file_object)
                    else:
                        plist = biplist.readPlist(plist_file_object)
                else:
                    try:
                        plist = nd.deserialize_plist(plist_file_object)
                    except (nd.DeserializeError, nd.biplist.NotBinaryPlistException, nd.biplist.InvalidPlistException,
                            nd.plistlib.InvalidFileException, nd.ccl_bplist.BplistError, ValueError, TypeError, OSError,
                            OverflowError) as ex:
                        print(f'Failed to read plist for {row[0]}, error was:' + str(ex))

                if plist:
                    if type(plist) is dict:
                        var1 = plist.get('bundleIdentifier', '')
                        var2 = plist.get('bundlePath', '')
                        var3 = plist.get('sandboxPath', '')

                        print(f'bundleIdentifier: {var1}')
                        print(f'bundlePath: {var2}')
                        print(f'sandboxPath: {var3}')
                    else:
                        print(f'For {row[0]} Unexpected type "' + str(
                            type(plist)) + '" found as plist root, can\'t process')

                else:
                    print(f'For {row[0]}, plist could not be read!')
        return var3
