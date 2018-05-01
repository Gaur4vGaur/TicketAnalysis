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
    return sorted(dict(col).items(), key=operator.itemgetter(1), reverse=True)[:5]

def findTotalMerges(msgs):
    c = 0
    for i in msgs:
        if('merge pull request' in i.lower()):
            c = c+1
                
    return c


def appStats(app):
    res = pd.read_excel('C:/1My/study/project/TicketAnalysis/commits/' + app + '.xlsx', 'Sheet1')
    table = res.groupby(['month']).agg({'name':len})
    totalMerges = findTotalMerges(res['comments'])
    totalCommits = len(res)
    (bi, tri) = appCommentsAnalysis(app, res)
    
    writeToExcel(app, table, totalMerges, totalCommits, bi, tri)
    
def writeToExcel(app, table, merges, commits, bi, tri):   
    workbook = xlsxwriter.Workbook('C:/1My/study/project/TicketAnalysis/commits/' + app + 'stats.xlsx')
    worksheet = workbook.add_worksheet()
    
    worksheet.write(0, 0, 'app')
    worksheet.write(0, 1, 'Jan')
    worksheet.write(0, 2, 'Feb')
    worksheet.write(0, 3, 'Mar')
    worksheet.write(0, 4, 'Apr')
    worksheet.write(0, 5, 'Merges')
    worksheet.write(0, 6, 'Commits')
    worksheet.write(0, 7, 'Tri')
    
    worksheet.write(1, 0, 'app')
    
    for rec in table.itertuples():
        month, count = rec
        worksheet.write(1, month, count)    
        
    worksheet.write(1, 5, merges)
    worksheet.write(1, 6, commits)
    worksheet.write(1, 7, tri)
        
    workbook.close()
    
def joinListItems(l):
    mapFirstEle = map(lambda x: x[0], l)
    newList = list(mapFirstEle)
    return ''.join(str(newList))

def appCommentsAnalysis(app, res):
    msgs = ''
    for index, d, n, c, m in res.itertuples():
        msgs += c
        
    word_sent = tokenizeSentences(msgs, app)    
    bigram = findSortedBigrams(word_sent)
    trigram = findSortedTrigrams(word_sent)
    
    mostUsedBigram = findMostUsed(bigram)
    mostUsedTrigram = findMostUsed(trigram)
    
    
    return (joinListItems(mostUsedBigram), joinListItems(mostUsedTrigram))


'''res.groupby(['date']).agg({'name':len})'''
'''res['date'].apply(lambda x: pd.to_datetime(x).month)'''