from TextExtract import *

from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns

#문장으로 잘라내기
text = "TextExtract에서 받은 text."
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



#######################################
def show_tweet_word_count_stat(data):
    num_word = []
    num_unique_words = []
    for item in data:
        num_word.append(len(str(item).split()))
        num_unique_words.append(len(set(str(item).split())))

    # 일반
    train['num_words'] = pd.Series(num_word)
    # 중복 제거
    train['num_unique_words'] = pd.Series(num_unique_words)

    x = data[0]
    x = str(x).split()
    print(len(x))

    rc('font', family='AppleGothic')

    fig, axes = plt.subplots(ncols=2)
    fig.set_size_inches(18, 6)
    print('Tweet 단어 평균 값 : ', train['num_words'].mean())
    print('Tweet 단어 중간 값', train['num_words'].median())
    sns.distplot(train['num_words'], bins=100, ax=axes[0])
    axes[0].axvline(train['num_words'].median(), linestyle='dashed')
    axes[0].set_title('Tweet 단어 수 분포')

    print('Tweet 고유 단어 평균 값 : ', train['num_unique_words'].mean())
    print('Tweet 고유 단어 중간 값', train['num_unique_words'].median())
    sns.distplot(train['num_unique_words'], bins=100, color='g', ax=axes[1])
    axes[1].axvline(train['num_unique_words'].median(), linestyle='dashed')
    axes[1].set_title('Tweet 고유한 단어 수 분포')

    plt.show()


show_tweet_word_count_stat(clean_processed_tweet)