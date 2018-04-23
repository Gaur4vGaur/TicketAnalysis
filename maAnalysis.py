#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 06:26:09 2018

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
import sentimentAnalysis as sa
import vaderSentiment as va

def cleanText(text):
    text = text.replace('What were you doing?:', ". ")
    text = text.replace('What do you need help with?:', ". ")
    text = re.sub("([.])", '. ', text)
    text = re.sub("(?:&nbsp;|<[^>]+>|[,])+", ' ', text)
    text = text.replace('\n', ". ")
    return text

def tokenizeText(text):
    return sent_tokenize(text)

def tokenizeSentences(text):
    word_sent = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation) + ['marriage', 'allowance', 'support', 'please'])
    
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

def printHelper(list):
    for entry in list:
        w,f = entry
        print(w)
    
    for entry in list:
        w,f = entry
        print(f)
    

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


res = pd.read_excel('ma.xlsx', 'Sheet1')
dataToExcel = []
length = {}
description = ''
descDict = {}

for index, tkt, date, desc, url in res.itertuples():
    cdesc = cleanText(desc)
    descDict[cdesc] = desc
    description += cdesc

sents = tokenizeText(description)    
word_sent = tokenizeSentences(description)

bigram = findSortedBigrams(word_sent)
trigram = findSortedTrigrams(word_sent)
freq = findStemWordsFreequency(word_sent)

mostUsed = findMostUsed(freq)
mostUsedBigram = findMostUsed(bigram)
mostUsedTrigram = findMostUsed(trigram)

printHelper(mostUsed)
print('\n')
printHelper(mostUsedBigram)
print('\n')
printHelper(mostUsedTrigram)
print('\n')

(pos, neg) = va.sentimentListCalculation(descDict.keys())

va.sentimentStats(pos, neg)
print('------------------------\n')
va.printExtremeFeedback(pos,descDict)
print('------------------------\n')
va.printExtremeFeedback(neg,descDict)



    
'''print(sorted(length.items(), key=operator.itemgetter(1)))'''