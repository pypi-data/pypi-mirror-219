import json
import yake
from sklearn.feature_extraction.text import TfidfVectorizer
from underthesea import word_tokenize
from rapidfuzz import fuzz
from kwextractor.utils.process_kw import *
from kwextractor.constants import FILE_EXTRACTED_KEYWORDS, FILE_STOP_WORDS, FILE_EMOTION_WORDS


class ExtractKeywords:
    def __init__(self, **kwargs):
        """
        Initialize the module

        :param kwargs: parameters for the module (stop_words, data_keywords, ngram, lan)

        - stop_words: a list of stop words
        - data_keywords: a dictionary of keywords - known words (type: [list of keywords])
        - ngram: number of ngram
        - lan: language of text
        """
        self.data_full_keywords = None
        self.data_keywords = None
        self.kw_extractor = None
        self.stop_words = None
        self.ngram = None
        self.tfidf = None
        self.lan = None
        self.return_group = False
        for k, v in kwargs.items():
            assert (k in ("stop_words", "data_keywords", "ngram", "lan"))
            setattr(self, k, v)
        self.initialize()

    def initialize(self):
        """
        Initialize the module

        :return: None
        """
        if not self.stop_words:
            with open(FILE_STOP_WORDS, 'r', encoding='utf-8') as f:
                self.stop_words = sort_keywords(f.read().splitlines())
        if not self.ngram:
            self.ngram = 2
        if not self.lan:
            self.lan = 'vi'
        if not self.data_keywords:
            with open(FILE_EXTRACTED_KEYWORDS, 'r', encoding='utf-8') as f:
                self.data_keywords = {'general': sort_keywords(json.load(f))}
            with open(FILE_EMOTION_WORDS, 'r', encoding='utf-8') as f:
                self.data_keywords['emotion'] = sort_keywords(f.read().splitlines())
        self.data_full_keywords = sort_keywords(merge_type_keywords(self.data_keywords))
        for k, v in self.data_keywords.items():
            self.data_keywords[k] = ' '.join(v).lower()
        self.kw_extractor = yake.KeywordExtractor(lan=self.lan, n=self.ngram, stopwords=self.stop_words)
        self.tfidf = TfidfVectorizer(stop_words=self.stop_words)

    def tfidf_case(self, text, from_yake):
        """
        Using tfidf to extract keywords from text.
        The method require a list of keywords from rule_case() method.
        The weight of each keyword is calculated by tfidf * number of times it appears in text.
        And the average weight of all keywords is threshold to decide whether a keyword is important.

        :param: text cleaned text and filtered by rule_case() method
        :param: from_rulebase list of keywords from rule_case() method
        :return: list of keywords
        """
        data_words = text.replace('.', '').replace('\t', '').split(" ")
        yake_kw = list(from_yake.keys())
        # use pre-extracted keywords for extracting faster
        for word in data_words:
            word = word.strip('_')
            if word.lower() in self.data_full_keywords:
                yake_kw.append(word.replace('_', ' '))
        # filter cases that have only one word in text after filtering stop words and special characters
        if len(data_words) == 1:
            return yake_kw
        # use tf-idf to extract keywords
        # (the average of a sentence's f-idf weights is the threshold for choosing keywords)
        count_kw = dict.fromkeys(data_words)
        for word in list(count_kw.keys()):
            count_kw[word.lower()] = data_words.count(word)
        result = self.tfidf.fit_transform(text.split("."))
        result = result.toarray().tolist()
        if hasattr(self.tfidf, 'get_feature_names_out'):
            feature_name = self.tfidf.get_feature_names_out()
        else:
            feature_name = self.tfidf.get_feature_names()
        array_sentence = text.replace('.', '').lower().strip(' ').split(' ')
        # filter in result
        new_weight = filter(lambda x: x[0] in array_sentence and x[0] in list(count_kw.keys()),
                            zip(feature_name, result))
        new_weight = list(new_weight)
        # new weight of a word calculate following formula:
        # (tf-idf weight of a word) * (number of times a word appears in a sentence)
        new_weight = [(x[0], x[1] * count_kw[x[0]]) for x in new_weight]
        # update weight if it is already in the extracted keywords list
        for word in yake_kw:
            for indexW, w in enumerate(new_weight):
                if word.lower() in w[0].lower() or w[0].lower() in word.lower():
                    if w[0].lower() in from_yake:
                        update_weight = (w[1] + from_yake[word]) / 2
                    else:
                        update_weight = [w_i + 0.01 for w_i in w[1]]
                    w = (w[0], update_weight)
                    new_weight[indexW] = w
        if not new_weight:
            return []
        # calculate average weight of all keywords
        new_weight = [(x[0], sum(x[1])) for x in new_weight]
        avg = sum([x[1] for x in new_weight]) / len(new_weight)
        # filter keywords that have weight > avg
        new_weight = filter(lambda x: x[1] >= avg - 0.01 and x[0] in list(count_kw.keys()), new_weight)
        new_weight = list(new_weight)
        # add keywords to extracted keywords list
        yake_kw = [x[0].replace('_', ' ') for x in new_weight] + yake_kw
        yake_kw = list(dict.fromkeys(yake_kw).keys())
        return yake_kw

    def filter_keywords(self, keywords, threshold=10):
        """
        Filter keywords that are noise words.

        Noise words are:

        - Longer than threshold or 10 characters
        - Shorter than 2 characters
        - Contain special characters
        - Contain stop words
        - Contain numbers
        - Contain only one character
        - Already exist in another keyword (substring)

        :param threshold: limit of number of characters in a keyword
        :param keywords: list of keywords
        :return: list of filtered keywords
        """
        keywords = [word for word in keywords if word not in ('', '\\n', '\\t', '\\r', ' ') and len(
            word) > 1 and word.replace(' ', '_') not in self.stop_words]
        wrong_keywords = []
        for i in range(len(keywords) - 1, -1, -1):
            char_break = ',;:.-_ '
            for char in char_break:
                if char in keywords[i]:
                    char_break = char
            if len(keywords[i].split(char_break)) > threshold:
                wrong_keywords.append(keywords[i])
            else:
                if ((char_break not in keywords[i]) and (len(keywords[i]) > 10)) or (
                        (char_break not in keywords[i]) and (len(keywords[i]) < 2)):
                    wrong_keywords.append(keywords[i])
        keywords = [word for word in keywords if word not in wrong_keywords]
        return keywords

    def merge_overlap_keywords(self, keywords, origin_text):
        """
        Merge keywords that are overlapping.

        Example: ['thất ngôn bát cú', 'bát cú đường luật'] -> ['thất ngôn bát cú đường luật']

        :param origin_text: cleaned text
        :param keywords: list of keywords
        :return: list of merged keywords
        """
        origin_text = origin_text.lower().replace('_', ' ')
        for kw in keywords:
            for kw2 in keywords:
                if kw != kw2:
                    try_merge = is_overlap(kw, kw2)
                    if try_merge and try_merge.lower() in origin_text:
                        keywords.remove(kw)
                        keywords.remove(kw2)
                        keywords.append(try_merge)
                        return self.merge_overlap_keywords(keywords, origin_text)
        return keywords

    def pipeline_default(self, text):
        """
        Extract keywords from text.

        :param: any text
        :return: list contains keywords
        """
        cleaned_text = clean_text(text)
        text_test = str(word_tokenize(cleaned_text, format="text"))
        text_test = " ".join(self.filter_keywords(text_test.split(' ')))
        if not text_test:
            return ''
        keywords_yake = dict(self.kw_extractor.extract_keywords(cleaned_text))
        text_test_keyword = self.tfidf_case(text_test, keywords_yake)
        text_test_keyword = sort_keywords(text_test_keyword)
        text_test_keyword = self.merge_overlap_keywords(text_test_keyword, text_test)
        text_test_keyword = remove_duplicate_keywords(text_test_keyword)
        text_test_keyword = self.merge_overlap_keywords(text_test_keyword, text_test)
        text_test_keyword = remove_duplicate_keywords(text_test_keyword)
        text_test_keyword = self.merge_overlap_keywords(text_test_keyword, text_test)
        text_test_keyword = self.filter_keywords(text_test_keyword)
        return text_test_keyword

    def label_group(self, kw_extracted):
        """
        Label groups by their keywords.

        :param kw_extracted: list of groups
        :return: a dictionary contains groups and their labels (e.g. {label : [keywords]})
        """
        labels = {}
        for kw in kw_extracted:
            # compare with self.data_keywords
            max_score = 0
            label_max = ''
            for label, keywords in self.data_keywords.items():
                if kw.replace(' ', '').isdigit():
                    label_max = 'number'
                    break
                fuzz_score = fuzz.token_set_ratio(kw.lower(), keywords.lower()) / 100
                if fuzz_score >= max_score:
                    max_score = fuzz_score
                    label_max = label
            print(label_max, max_score)
            if label_max in labels:
                labels[label_max].extend([kw])
            else:
                labels[label_max] = [kw]
        return labels

    def extract_keywords(self, text):
        """
        Check if a sentence of a paragraph. And run pipeline for getting keywords.

        :param text: any text
        :return: string contains keywords that are separated by comma (if text is a sentence)
        :return: list of keywords (if text is a paragraph)
        """
        text = text.strip('.')
        kw_ex = self.pipeline_default(text)
        if kw_ex:
            if self.return_group:
                lb_groups = self.label_group(kw_ex)
                if 'general' not in lb_groups:
                    return lb_groups
            return ','.join(kw_ex)
        return ''

