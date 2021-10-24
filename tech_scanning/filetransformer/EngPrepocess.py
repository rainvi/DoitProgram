from TextExtract import *

import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

class EngPreprocess:

    def __init__(self, file_path):
        self.file_path = file_path;

    #파일 확장자 확인하고 문자들 추출하기.
    def data_extract(self):
        text = TextExtract()
        if os.path.splitext(self.file_path).equals(".pdf"):
            extracted_text = text.get_pdf_text()
        elif os.path.splitext(self.file_path).equals(".hwp"):
            extracted_text = text.get_hwp_text()
        elif os.path.splitext(self.file_path).equals(".docx"):
            extracted_text = text.get_docx_text()
        else:
            return
        return extracted_text


    ##데이터 전처리##
    ##토큰화 -> 불용어 제거 -> 어간 추출 및 중복 제거 stemming ->표제어 추출 및 중복 제거 lemmatization -> 대소문자 통합
    def data_clear(text):
        # 단어 단위로 토큰 생성 (문장 한 줄당 배열 하나 배정. 2차원 배열)
        tokens = [word for sent in nltk.sent_tokenize(text)
                  for word in nltk.word_tokenize(sent)]

        # 불용어 제거
        stop = stopwords.words('english')
        tokens = [token for token in tokens if token not in stop]

        # 소문자로 데이터 맞추기.
        tokens = [word.lower() for word in tokens]

        # lemmatization
        lmtzr = WordNetLemmatizer()
        tokens = [lmtzr.lemmatize(word) for word in tokens]
        tokens = [lmtzr.lemmatize(word, 'v') for word in tokens]

        # stemming
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for word in tokens]

        preprocessed_text = ' '.join(tokens)
        return preprocessed_text

    def propressing(self):
        my_text = self.data_extract(self.file_path)
        preprocessed_text = self.data_clear(my_text)
        return preprocessed_text