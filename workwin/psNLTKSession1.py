# -*- coding: utf-8 -*-


import nltk

text="Marry is little. Marry had a little lamb. Her fleece was as white as snow."
from nltk.tokenize import word_tokenize, sent_tokenize

"""tokenize sentence and words"""
sents=sent_tokenize(text)
words = word_tokenize(text)

"""Get rid of punctuation and stopwords"""
from nltk.corpus import stopwords
from string import punctuation
customStopWords=set(stopwords.words('english')+list(punctuation))

wordsWOStopwords=[word for word in word_tokenize(text) if word not in customStopWords]
print(wordsWOStopwords)

"""Bigrams"""
from nltk.collocations import BigramCollocationFinder
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(wordsWOStopwords)
bigram = sorted(finder.ngram_fd.items())

for w in bigram:
    (a,b) = w


"""stem words"""
text2 = "Mary closed on closing night when she was in the mood to close."
from nltk.stem.lancaster import LancasterStemmer
st=LancasterStemmer()
stemmedWords=[st.stem(word) for word in word_tokenize(text2)]
print(stemmedWords)
    

