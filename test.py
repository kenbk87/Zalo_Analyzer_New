import json
import re


def remove_ascii_non_printable(chunk):
    """
    Remove non-ascii
    """
    chunk = ' '.join(chunk.split())
    return ''.join([ch for ch in chunk if 31 < ord(ch) < 126 or ord(ch) == 9])


str_encode = b'\x00\x00\x00\x06\x00\x00\x01\x99\x00\x00\x00,\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00.\x00\x00\x00\xed{""width"":859,""height"":1908,""is_group_layout"":0,""group_layout_id"":-1,""id_in_group"":0,""total_item_in_group"":0,""fileValid"":1,""contentId"":""4674"",""result_qr_code"":"""",""center_qr_point_x"":0,""center_qr_point_y"":0,""is_has_decoded_qr_view_full"":0}\x00\x00\x000\x00\x00\x00Chttps://f25-zpc.zdn.vn/8395944660500680746/9c6f2066f9cc37926edd.jpg\x00\x00\x001\x00\x00\x00Ehttps://t-f25-zpc.zdn.vn/8395944660500680746/9c6f2066f9cc37926edd.jpg\x00\x00\x00\r\x00\x00\x00\xe9{""s"":0,""ds"":36,""ld"":{""lat"":0,""lon"":0},""ofs"":{""ct"":1650538401000,""di"":0,""e"":""jpg"",""fn"":""Screenshot_20220421-175321_MB Bank"",""h"":2400,""la"":0,""lo"":0,""po"":0,""s"":620460,""t"":0,""w"":1080,""ss"":3,""vc"":"""",""vb"":0,""vfr"":0,""vl"":0,""vp"":0,""scsh"":1}}\x00\x00\x00\x0f\x00\x00\x00?\x00\x00\x00\xbf\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\xc0\x00\x00\x00\x02\x00\x00\x00\x00\x00\xc3\x00\x00\x00\x01\x00\x00\x00\x00\xc6\x00\x00\x00\x02\x00\x00\x00\x00\x00\xc7\x00\x00\x00\x02\xff\xff\x00\x00\x00\xca\x00\x00\x00\x04\x00\x00\x00\x00'
str_decode = str_encode.decode('utf-8', 'ignore')

str_decode = remove_ascii_non_printable(str_decode)
print(str_decode)
