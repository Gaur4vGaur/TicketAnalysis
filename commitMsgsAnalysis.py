#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 06:04:31 2018

@author: gaurav
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
import xlsxwriter
import re

def tokenizeText(text):
    return sent_tokenize(text)

def tokenizeSentences(text, app):
    word_sent = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation) + ['merge', app, 'pull', 'request', 'branch', 'master'])
    
    word_sent=[word for word in word_sent if word not in _stopwords]
    return word_sent

def findSortedBigrams(words):
    finder = BigramCollocationFinder.from_words(words)
    return finder.ngram_fd.items()

def findSortedTrigrams(words):
    finder = TrigramCollocationFinder.from_words(words)
    return finder.ngram_fd.items()
    
def findStemWordsFreequency(words):
    st = LancasterStemmer()
    stemmedWords = [st.stem(word) for word in words]
    return FreqDist(stemmedWords)

def findMostUsed(col):
    return sorted(dict(col).items(), key=operator.itemgetter(1), reverse=True)[:10]

def findTotalMerges(msgs):
    c = 0
    for i in msgs:
        if('merge pull request' in i.lower()):
            c = c+1
                
    return c


def appStats(app):
    res = pd.read_excel('commits/' + app + '.xlsx', 'Sheet1')
    table = res.groupby(['month']).agg({'name':len})
    totalMerges = findTotalMerges(res['comments'])
    totalCommits = len(res)

def appCommentsAnalysis(app):
    res = pd.read_excel('commits/' + app + '.xlsx', 'Sheet1')
    msgs = ''
    for index, d, n, c in res.itertuples():
        msgs += c

    sents = tokenizeText(msgs)    
    word_sent = tokenizeSentences(msgs, app)
    
    bigram = findSortedBigrams(word_sent)
    trigram = findSortedTrigrams(word_sent)
    freq = findStemWordsFreequency(word_sent)
    
    mostUsed = findMostUsed(freq)
    mostUsedBigram = findMostUsed(bigram)
    mostUsedTrigram = findMostUsed(trigram)


'''res.groupby(['date']).agg({'name':len})'''
'''res['date'].apply(lambda x: pd.to_datetime(x).month)'''