#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 20:02:25 2018

@author: gaurav
"""

import urllib.request
import pandas as pd
import xlsxwriter

def fetchLinks(url):
    response = urllib.request.urlopen(url)
    count = 0
    linkList = [url]
    link = response.getheader('Link')
    
    while(link is not None):
        if('next' not in link):
            break
        
        for l in link.split(', '):
            if('next' in l):
                count = count + 1
                url = l.split(';')[0]
                url = url.replace('<', '').replace('>','')
                linkList.append(url)
                response = urllib.request.urlopen(url)
                link = response.getheader('Link')
                if(count == 10):
                    break
    print('links gone')
    return linkList
        
    

def fetchServiceNamesLiveServices(links):
    
    repo = []
    commit = []
    for l in links:
        lsJson = pd.read_json(l)
        repo = repo + lsJson['name'].tolist()
        commit = commit + lsJson['commits_url'].tolist()
    return (repo, commit)
    


def writeToExcel(r, c):
    row = 1
    col = 0
    
    workbook = xlsxwriter.Workbook('liveServicesRepo.xlsx')
    worksheet = workbook.add_worksheet()
    
    worksheet.write(0, 0, 'name')
    worksheet.write(0, 1, 'commitUrl')
    
    for n,u in zip(r,c):
        u = u.replace('{/sha}', '')
        worksheet.write(row, col,     n)
        worksheet.write(row, col + 1, u)
        row += 1
        
    workbook.close()
    
'''print(response.getheaders()[0])
print(type(response.getheader('Link')))
lsJson = pd.read_json("https://api.github.com/teams/2146742/repos?access_token=<token>")'''

links = fetchLinks("https://api.github.com/teams/2146742/repos?access_token=<token>")
(r,c) = fetchServiceNamesLiveServices(links)
writeToExcel(r,c)

'''for key, value in pdJson['commit'].items():
    print(value['author']['date'], value['message'])'''