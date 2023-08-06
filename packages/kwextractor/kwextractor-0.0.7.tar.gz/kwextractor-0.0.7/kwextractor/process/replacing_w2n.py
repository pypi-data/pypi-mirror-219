from vietnam_number import w2n, n2w
from kwextractor.process.extract_keywords import ExtractKeywords, clean_text


class ReplacingWtoN:
    def __init__(self):
        self.exkeywords = ExtractKeywords()

    def replacing_w2n(self, text):
        """
        Replace number in text by number in vietnamese.
        :param text: text to replace
        :return text: text after replacing
        """
        text = clean_text(text)
        kw = self.exkeywords.extract_keywords(text).split(',')
        num = None
        for i in kw:
            try:
                try_convert = w2n(i)
                if isinstance(try_convert, int):
                    num = str(try_convert)
                    kw = i
                    break
            except ValueError:
                pass
        if num is not None:
            text_prefix = text.split(kw.split(' ')[0])[0]
            try:
                prefix_num = str(w2n(text_prefix))
            except ValueError:
                prefix_num = None
            if prefix_num is not None:
                if int(prefix_num) != int(num):
                    num = num.replace(num[0], prefix_num)
                    index_start = text.index(n2w(prefix_num))
                    index_end = text.index(kw.split(' ')[-1])
                    text = text[:index_start] + num + text[index_end + len(kw.split(' ')[-1]):]
            else:
                text = text.replace(kw, num)
        return text
