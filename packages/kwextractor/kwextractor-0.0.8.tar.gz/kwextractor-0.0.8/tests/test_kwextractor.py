from kwextractor.process.extract_keywords import ExtractKeywords
from kwextractor.process.extract_numverse import ExtractNumverse
from kwextractor.process.replacing_w2n import ReplacingWtoN


def test_vietnamese_extract_keywords():
    text = "tôi thích nghe các bản nhạc của Trịnh Công Sơn"
    keywords = ExtractKeywords().extract_keywords(text)
    assert keywords == "bản nhạc,Trịnh Công Sơn"
    text = "tôi thích nghe các bản nhạc của Trịnh Công Sơn và Thanh Nhã"
    keywords = ExtractKeywords().extract_keywords(text)
    assert keywords == "bản nhạc,Thanh Nhã,Trịnh Công Sơn"


def test_english_extract_keywords():
    text = "I want to buy an apple"
    keywords = ExtractKeywords().extract_keywords(text)
    assert keywords == "apple,want,buy,to"


def test_vietnamese_extract_numverse():
    text = "sinh cho tui bài thơ gồm hai chục câu nhé"
    num = ExtractNumverse().extract_numverse(text, 4)
    assert num == 4
    num = ExtractNumverse().extract_numverse(text, 20)
    assert num == 20


def test_vietnamese_replacing_w2n():
    text = "cho hỏi làm sao để sinh ra mười bài thơ"
    text = ReplacingWtoN().replacing_w2n(text)
    assert text == "cho hỏi làm sao để sinh ra 10 bài thơ"
