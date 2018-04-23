#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 23:08:46 2018

@author: gaurav
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from string import punctuation

from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict

articleURL: str = "https://www.washingtonpost.com/news/the-switch/wp/2016/10/18/the-pentagons-massive-new-telescope-is-designed-to-track-space-junk-and-watch-out-for-killer-asteroids/"

"""clean the web article may not be needed"""
def getTextWaPo(url):
    page = urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(page,"lxml")
    text = ' '.join(map(lambda p: p.text, soup.find_all('article')))
    return text.replace("?"," ")

"""Important function to fetch context of messages"""
def summarize(text, n):
    sents = sent_tokenize(text)
    assert n <= len(sents)
    word_sent = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation))

    """freequencies of words"""
    word_sent=[word for word in word_sent if word not in _stopwords]
    freq = FreqDist(word_sent)

    ranking = defaultdict(int)

    for i,sent in enumerate(sents):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] += freq[w]

    sents_idx = nlargest(n, ranking, key=ranking.get)
    return [sents[j] for j in sorted(sents_idx)]

 
article = getTextWaPo(articleURL)

print(summarize(article, 3))
