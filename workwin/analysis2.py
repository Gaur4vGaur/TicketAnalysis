# -*- coding: utf-8 -*-
"""
create most hit across all the tickets

@author: gaurav.gaur
"""

import pandas as pd

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation

from heapq import nlargest
from collections import defaultdict
from nltk.probability import FreqDist
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import TrigramCollocationFinder
from nltk.stem.lancaster import LancasterStemmer

import operator

def cleanAndTokenizeText(text):
    text = text.replace('What were you doing?:', ". ")
    text = text.replace('What do you need help with?:', ". ")
    text = text.replace('\n', ". ")
    return sent_tokenize(text)

def cleanAndTokenizeSentences(text):
    word_sent = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation) + ['need', 'help', 'trying', 'try'])
    
    word_sent=[word for word in word_sent if word not in _stopwords]
    return word_sent

def findSortedBigrams(words):
    finder = BigramCollocationFinder.from_words(words)
    return finder.ngram_fd.items()

def findTrigrams(words):
    finder = TrigramCollocationFinder.from_words(words)
    return finder.ngram_fd.items()
    
def findStemWordsFreequency(words):
    st = LancasterStemmer()
    stemmedWords = [st.stem(word) for word in word_sent]
    return FreqDist(stemmedWords)

def findMostUsed(col):
    return sorted(dict(col).items(), key=operator.itemgetter(1), reverse = True)[:5]

def summarizeText(sents, freq):
    ranking = defaultdict(int)
    impSent = ''
    
    if(len(sents) > 1):
        for i,sent in enumerate(sents):
            for w in word_tokenize(sent.lower()):
                if w in freq:
                    ranking[i] += freq[w]

        sents_idx = nlargest(1, ranking, key=ranking.get)
        if(len(sents_idx) > 0): 
            impSent = sents[sents_idx[0]]
            
        if(len(impSent) > 150): 
            impSent = impSent[0:150]
            
    return impSent

def printRes(records):
    for words, occ in records:
        print(words)
        
    for words, occ in records:
        print(occ)


res = pd.read_excel('C:/1My/study/project/analysis/My1.xlsx', 'Sheet3')
dataToExcel = []
description = ""

for index, desc, url in res.itertuples():
    
    description += desc + ". "
    
    
sents = cleanAndTokenizeText(description)
word_sent = cleanAndTokenizeSentences(description)

bigram = findSortedBigrams(word_sent)
trigram = findTrigrams(word_sent)
freq = findStemWordsFreequency(word_sent)
wordFreq = FreqDist(word_sent)

mostUsedStem = sorted(dict(freq).items(), key=operator.itemgetter(1), reverse = True)[:15]
mostUsed = sorted(dict(wordFreq).items(), key=operator.itemgetter(1), reverse = True)[:15]
bigrams = findMostUsed(bigram)
trigrams = findMostUsed(trigram)

print(mostUsedStem)
print('\n\n')
printRes(bigrams)
print('\n\n')
printRes(trigrams)
