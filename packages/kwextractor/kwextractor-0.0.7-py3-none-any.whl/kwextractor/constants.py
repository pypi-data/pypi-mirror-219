import os
WORK_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
FILE_EXTRACTED_KEYWORDS = os.path.join(WORK_DIR,"kwextractor","data","data_full_allkeywords.txt")
FILE_EMOTION_WORDS = os.path.join(WORK_DIR,"kwextractor","data","data_emotion_words.txt")
FILE_STOP_WORDS = os.path.join(WORK_DIR,"kwextractor","data","stop_words_vn_tokenized.txt")
