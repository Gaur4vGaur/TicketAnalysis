#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 22:01:27 2018

@author: gaurav
"""
import pandas as pd
import xlsxwriter

'''pd.read_json('https://api.github.com/repos/hmrc/tai/commits')'''

def commitMessages(url):
    json = None
    
    try:
        json = pd.read_json(url)
    except:
        json = None
        

    messages = []
    isPreviousYear = False
    
    if(json is not None or json.empty):
        return (messages, True)
    
    for key, value in json['commit'].items():
        t = pd.to_datetime(value['author']['date'])
        messages.append((value['author']['date'], value['author']['name'], value['message']))
        if(t.year != 2018):
            isPreviousYear = True
            break;
    
    return (messages, isPreviousYear)
    
def writeToExcel(app, msgs):
    row = 1
    col = 0
    
    workbook = xlsxwriter.Workbook('commits/' + app + '.xlsx')
    worksheet = workbook.add_worksheet()
    
    worksheet.write(0, 0, 'date')
    worksheet.write(0, 1, 'name')
    worksheet.write(0, 2, 'comments')
    worksheet.write(0, 3, 'month')
    
    for msg in msgs:
        d,n,c = msg
        worksheet.write(row, col,     d)
        worksheet.write(row, col + 1, n)
        worksheet.write(row, col + 2, c)
        worksheet.write(row, col + 3, pd.to_datetime(d).month)
        row += 1
        
    workbook.close()
    
def commitsForYear(app, appUrl):
    (messages, isPreviousYear) = commitMessages(appUrl)
    c = 1;
    
    while(not isPreviousYear):
        c = c+1
        u = appUrl + '?page=' + str(c)
        print(u)
        (m, i) = commitMessages(u)
        messages = messages + m
        isPreviousYear = i
        
    writeToExcel(app, messages)
    return messages

