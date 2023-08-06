import re
from kwextractor.process.replacing_w2n import ReplacingWtoN

class ExtractNumverse:
    def __init__(self):
        self.repw2n = ReplacingWtoN()

    def extract_numverse(self, text, maximum=100):
        """
        Extract number of verse from text.
        This method will call extract_keywords to extract keywords.
        Then connect them to a full text and extract number of verse by using vietnam_number library.
        :param text: text to extract number of verse
        :param maximum: maximum return value
        :return num: number of verse
        :return bool: False if number of verse is not found.
        """
        text = self.repw2n.replacing_w2n(text)
        num = re.findall(r'\d+', text)
        if num:
            num = int(num[0])
            if num > maximum:
                return maximum
            return num
        return 0
