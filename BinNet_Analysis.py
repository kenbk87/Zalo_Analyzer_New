class BinNet_Analysis:
    """
    : Phân tích dữ liệu trong cột BinNet:
    """

    def __init__(self, data):
        self.data = data

    @staticmethod
    def remove_ascii_non_printable(chunk):
        """
        Remove non-ascii
        """
        chunk = ' '.join(chunk.split())
        return ''.join([ch for ch in chunk if 31 < ord(ch) < 126 or ord(ch) == 9])

    def convert_BinNet(self):
        """
        :return:
        """
        str_decode = self.data.decode('utf-8', 'ignore')
        str_final = self.remove_ascii_non_printable(str_decode)
        return str_final
