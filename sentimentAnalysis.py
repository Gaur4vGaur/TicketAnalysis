#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 07:45:40 2018

@author: gaurav
"""

from nltk.corpus import sentiwordnet as swn
import operator
import re

def naiveSentiment(feedback):
 reviewPolarity = 0.0
 numExceptions = 0
 for word in feedback.lower().split():
   numMeanings = 0
   
   weight = 0.0
   try:
     for meaning in swn.senti_synsets(word):
       if meaning.pos_score() > meaning.neg_score():
          weight = weight + (meaning.pos_score() - meaning.neg_score())
          numMeanings = numMeanings + 1
       elif meaning.pos_score() < meaning.neg_score():
          weight = weight - (meaning.neg_score() - meaning.pos_score())
          numMeanings = numMeanings + 1
   except: 
       numExceptions = numExceptions + 1
   if numMeanings > 0:
     reviewPolarity = reviewPolarity + (weight/numMeanings)
 return reviewPolarity

'''given a list creates a map with all positive and negative reviews'''
def sentimentListCalculation(feedbacks):
    pos = {}
    neg = {}
    
    for fd in feedbacks:
        score = naiveSentiment(fd)
        if(score > 0):
            pos[fd] = score
        else:
            neg[fd] = score
            
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
        print(k)
        print(v)
        print('\n')


'''examples on how to use'''
review = "this is the best restaurant in the city"
naiveSentiment(review)

negatedReview = "this is not the best restaurant in the city"
naiveSentiment(negatedReview)

negatedReview = "this is not the worst restaurant in the city"
naiveSentiment(negatedReview)


