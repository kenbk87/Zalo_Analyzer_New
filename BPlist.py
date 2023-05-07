import biplist
import io
import nska_deserialize as nd
import plistlib
import sys


class BPlist_Parse:
    def __init__(self, bplist):
        self.bplist = bplist

    def parse(self):
        # BytesIO được sử dụng với dữ liệu binary:
        plist_file_object = io.BytesIO(self.bplist)
        if self.bplist.find(b'NSKeyedArchiver') == -1:
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
                logfunc(f'Failed to read plist for {self.bplist}, error was:' + str(ex))
        return plist
