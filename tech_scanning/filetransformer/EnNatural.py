from TextExtract import *

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
from collections import Counter

text = "text 경로, 텍스트 str화 해서 text변수에 " \
       "저장."
#배열 출력
word_list_en = word_tokenize(text)
sentence_list_en = sent_tokenize(text)
#word_tokenize(text) // 단어 토큰화
#pos_tag(tokenized_sentence) // (단어, 품사) 토큰화

#표제어 추출
lemmatizer = WordNetLemmatizer()
result = [lemmatizer.lemmatize(w) for w in word_list_en]

#어간 추출

#불용어 제거하기.
#stop word는 강계 찾아보면서 더 추가해두기. 아니면 메모장txt에 불용어 리스트 저장해서 불러와서 쓰는 것도 좋다.
stop_words = "any if or i wer was are am "
stop_words = set(stop_words.split(' '))

result = [word for word in word_list_ko if not word in stop_words]

vocab = {}
preprocessed_sentences = []
stop_words = set(stopwords.words('english'))

for sentence in sentences:
    # 단어 토큰화
    tokenized_sentence = word_tokenize(sentence)
    result = []

    for word in tokenized_sentence:
        word = word.lower() # 모든 단어를 소문자화하여 단어의 개수를 줄인다.
        if word not in stop_words: # 단어 토큰화 된 결과에 대해서 불용어를 제거한다.
            if len(word) > 2: # 단어 길이가 2이하인 경우에 대하여 추가로 단어를 제거한다.
                result.append(word)
                if word not in vocab:
                    vocab[word] = 0
                vocab[word] += 1
    preprocessed_sentences.append(result)
vocab_sorted = sorted(vocab.items(), key = lambda x:x[1], reverse = True)
word_to_index = {}
i = 0
for (word, frequency) in vocab_sorted :
    if frequency > 1 : # 빈도수가 작은 단어는 제외.
        i = i + 1
        word_to_index[word] = i

vocab_size = 5
words_frequency = [word for word, index in word_to_index.items() if index >= vocab_size + 1] # 인덱스가 5 초과인 단어 제거
for w in words_frequency:
    del word_to_index[w] # 해당 단어에 대한 인덱스 정보를 삭제
word_to_index['OOV'] = len(word_to_index) + 1

encoded_sentences = []
for sentence in preprocessed_sentences:
    encoded_sentence = []
    for word in sentence:
        try:
            encoded_sentence.append(word_to_index[word])
        except KeyError:
            encoded_sentence.append(word_to_index['OOV'])
    encoded_sentences.append(encoded_sentence)

all_words_list = sum(preprocessed_sentences, [])
vocab = Counter(all_words_list)
vocab_size = 5
vocab = vocab.most_common(vocab_size) # 등장 빈도수가 높은 상위 5개의 단어만 저장

word_to_index = {}
i = 0
for (word, frequency) in vocab :
    i = i + 1
    word_to_index[word] = i

all_words_list = sum(preprocessed_sentences, [])
print(all_words_list)
vocab = Counter(all_words_list)
vocab_size = 5
vocab = vocab.most_common(vocab_size) # 등장 빈도수가 높은 상위 5개의 단어만 저장
word_to_index = {}
i = 0
for (word, frequency) in vocab :
    i = i + 1
    word_to_index[word] = i

print(word_to_index)


