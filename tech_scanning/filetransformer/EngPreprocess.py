from TextExtract import *

import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

class EngPreprocess:

    def __init__(self, file_path):
        te = TextExtract(file_path)
        self.ET = te

    #파일 확장자 확인하고 문자들 추출하기.
    def data_extract(self):
        text = TextExtract(self.ET.file_path)
        file_name, file_ext = os.path.splitext(self.ET.file_path)
        if file_ext == ".pdf":
            extracted_text = text.get_pdf_text()
        elif file_ext == ".hwp":
            extracted_text = text.get_hwp_text()
        elif file_ext == ".doc":
            extracted_text = text.get_docx_text()
        else:
            return
        return extracted_text


    ##데이터 전처리##
    ##토큰화 -> 불용어 제거 -> 어간 추출 및 중복 제거 stemming ->표제어 추출 및 중복 제거 lemmatization -> 대소문자 통합
    def data_clear(self, text):
        # 단어 단위로 토큰 생성 (문장 한 줄당 배열 하나 배정. 2차원 배열)
        tokens = [word for sent in nltk.sent_tokenize(text)
                  for word in nltk.word_tokenize(sent)]

        # 불용어 제거
        #nltk.download('stopwords')
        stop = stopwords.words('english')
        tokens = [token for token in tokens if token not in stop]

        # 소문자로 데이터 맞추기.
        tokens = [word.lower() for word in tokens]

        # lemmatization
        #nltk.download('wordnet')
        lmtzr = WordNetLemmatizer()
        tokens = [lmtzr.lemmatize(word) for word in tokens]
        tokens = [lmtzr.lemmatize(word, 'v') for word in tokens]

        # stemming
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for word in tokens]

        preprocessed_text = ' '.join(tokens)
        return preprocessed_text

    def propressing(self):
        my_text = self.data_extract()
        preprocessed_text = self.data_clear(my_text)
        return preprocessed_text


"""검산 코드
my_text_path = "C:/Users/wonai/mystatus/Doit_program/tech_scanning/filetransformer/practice.hwp"
te = TextExtract(my_text_path)
ep = EngPreprocess(my_text_path)
print(ep.data_clear(ep.data_extract()))
"""
