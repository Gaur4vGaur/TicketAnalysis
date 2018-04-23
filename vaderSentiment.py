#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 08:51:13 2018

@author: gaurav
"""

from nltk.sentiment import vader
import operator
import re
from nltk.tokenize import word_tokenize




def sentimentListCalculation(feedbacks):
    pos = {}
    neg = {}
    sia = vader.SentimentIntensityAnalyzer()
    
    for fd in feedbacks:
        score = sia.polarity_scores(fd)
        count = len(word_tokenize(fd))
        if(score['compound'] > 0):
            pos[fd] = score['pos']
        else:
            neg[fd] = score['neg']
            
    return (pos, neg)

def sentimentStats(pos, neg):
    print(sum(pos.values()))
    print(sum(neg.values()))
    
def printExtremeFeedback(col, descDict):
    topFeedback = sorted(dict(col).items(), key=operator.itemgetter(1), reverse=True)[:3]
    
    for fd in topFeedback:
        k,v = fd
        text = descDict[k] 
        text = re.sub("(?:&nbsp;|<[^>]+>)+", '', text)
        print(text)
        print(v)
        print('\n')