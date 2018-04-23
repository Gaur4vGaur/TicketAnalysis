#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 21:12:34 2018

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
from nltk.stem.lancaster import LancasterStemmer

import operator
import xlsxwriter

def cleanAndTokenizeText(text):
    text = text.replace('What were you doing?:', ". ")
    text = text.replace('What do you need help with?:', ". ")
    text = text.replace('\n', ". ")
    return sent_tokenize(text)

def cleanAndTokenizeSentences(text):
    word_sent = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation))
    
    word_sent=[word for word in word_sent if word not in _stopwords]
    return word_sent

def findSortedBigrams(words):
    finder = BigramCollocationFinder.from_words(words)
    return sorted(finder.ngram_fd.items())
    
def findStemWordsFreequency(words):
    st = LancasterStemmer()
    stemmedWords = [st.stem(word) for word in word_sent]
    return FreqDist(stemmedWords)

def findMostUsed(col):
    return max(dict(col).items(), key=operator.itemgetter(1))[0]

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

def writeToExcel(data):
    row = 1
    col = 0
    
    workbook = xlsxwriter.Workbook('analysis.xlsx')
    worksheet = workbook.add_worksheet()
    
    worksheet.write(0, 0, 'description')
    worksheet.write(0, 1, 'url')
    worksheet.write(0, 2, 'most used word')
    worksheet.write(0, 3, 'most used words')
    worksheet.write(0, 4, 'sentence')
    
    for desc, url, word, bigram, impSent in data:
        w1, w2 = bigram
        worksheet.write(row, col,     desc)
        worksheet.write(row, col + 1, url)
        worksheet.write(row, col + 2, word)
        worksheet.write(row, col + 3, w1 + ' ' + w2)
        worksheet.write(row, col + 4, impSent)
        row += 1
        
    workbook.close()


res = pd.read_excel('my1.xlsx', 'Sheet3')
dataToExcel = []
length = {}
l = 0

for index, desc, url in res.itertuples():
    
    words = word_tokenize(desc.lower())
    l += len(words)
    
    sents = cleanAndTokenizeText(desc)    
    word_sent = cleanAndTokenizeSentences(desc)
    
    bigram = findSortedBigrams(word_sent)
    freq = findStemWordsFreequency(word_sent)
    
    mostUsed = findMostUsed(freq)
    mostUsedBigram = findMostUsed(bigram)
    
    summary = summarizeText(sents, freq)
    dataToExcel.append((desc, url, mostUsed , mostUsedBigram, summary))
    
    length[index+2] = len(desc)
    
print(l)
print(type(res))
    
'''print(sorted(length.items(), key=operator.itemgetter(1)))'''