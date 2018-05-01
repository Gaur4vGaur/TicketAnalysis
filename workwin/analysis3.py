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
import xlsxwriter

def cleanAndTokenizeText(text):
    text = text.replace('What were you doing?:', ". ")
    text = text.replace('What do you need help with?:', ". ")
    text = text.replace('\n', ". ")
    return sent_tokenize(text)

def cleanAndTokenizeSentences(text):
    word_sent = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation) + ['need', 'help', 'trying', 'try', 'could', 'quick', 'easy', 'use', "n't", 'straight', 'forward'])
    
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
        

res = pd.read_excel('C:/1My/study/project/analysis/3.xlsx', 'Sheet3')

def writeToExcel(data):
    row = 1
    col = 0
    
    workbook = xlsxwriter.Workbook('C:/1My/study/project/a3.xlsx')
    worksheet = workbook.add_worksheet()
    
    worksheet.write(0, 0, 'time')
    worksheet.write(0, 1, 'detail.origin')
    worksheet.write(0, 2, 'detail.recommendRating')
    worksheet.write(0, 3, 'detail.reasonForRating')
    
    for time, origin, rating, desc in data:
        worksheet.write(row, col,     time)
        worksheet.write(row, col + 1, origin)
        worksheet.write(row, col + 2, rating)
        worksheet.write(row, col + 3, desc)
        row += 1
        
    workbook.close()



def fitlerDescription(res):
    record = 0
    description = ""
    for index, time, origin, rating, desc in res.itertuples():
        lowerDesc = str(desc).lower()
        if('savings' in lowerDesc or 'untaxed' in lowerDesc or 'bank interest' in lowerDesc or 'building society' in lowerDesc):
            description += lowerDesc + ". "
            record += 1
    return (description, record)
    
def nonFitlerDescription(res):
    record = 0
    description = ""
    for index, time, origin, reason, desc in res.itertuples():
        lowerDesc = str(desc).lower()
        description += lowerDesc + ". "
        record += 1
        
    return (description, record)

def fitlerDataForXlsAutumn(res):
    record = 0
    dataToExcel = []
    for index, time, origin, rating, desc in res.itertuples():
        lowerDesc = str(desc).lower()
        if('savings' in lowerDesc or 'untaxed' in lowerDesc or 'bank interest' in lowerDesc or 'building society' in lowerDesc):
            record += 1
            dataToExcel.append((time, origin, rating, desc))
    
    print(record)
    return dataToExcel


dataToExcel = fitlerDataForXlsAutumn(res)
writeToExcel(dataToExcel)

'''description, record = nonFitlerDescription(res)
sents = cleanAndTokenizeText(description)
word_sent = cleanAndTokenizeSentences(description)

bigram = findSortedBigrams(word_sent)
trigram = findTrigrams(word_sent)
freq = findStemWordsFreequency(word_sent)
wordFreq = FreqDist(word_sent)

mostUsedStem = findMostUsed(freq)
mostUsed = findMostUsed(wordFreq)
bigrams = findMostUsed(bigram)
trigrams = findMostUsed(trigram)

print(record)
print('\n\n')
printRes(bigrams)
print('\n\n')
printRes(trigrams)'''



