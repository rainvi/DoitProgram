from TextExtract import *

import os

from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re
import nltk


#파일 확장자 확인하고 문자들 추출하기.
text = TextExtract()
file_path = "파일 경로 삽입."
if os.path.splitext(file_path).equals(".pdf"):
    extracted_text = text.get_pdf_text()
elif os.path.splitext(file_path).equals(".hwp"):
    extracted_text = text.get_hwp_text()
elif os.path.splitext(file_path).equals(".docx"):
    extracted_text = text.get_docx_text()

#문장으로 잘라내기

tokenized_sentences = sent_tokenize(text)
tokenized_words = []
for line in tokenized_sentences:
    tokenized_words.append(word_tokenize(line))


##데이터 전처리
def text_cleaning(text):
    only_english = re.sub('[^a-zA-Z]', ' ', text)
    no_capitals = only_english.lower().split()

    stops = set(stopwords.words('english'))
    no_stops = [word for word in no_capitals if not word in stops]
    # nltk.download('stopwords')
    stemmer = nltk.stem.SnowballStemmer('english')
    stemmer_words = [stemmer.stem(word) for word in no_stops]

    # 공백으로 구분된 문자열로 결합하여 결과 반환
    return ' '.join(stemmer_words)


