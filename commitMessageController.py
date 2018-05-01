# -*- coding: utf-8 -*-
"""
Created on Tue May  1 15:31:31 2018

@author: gaurav.gaur
"""

import pandas as pd
import commitMessage
import commitMsgsAnalysis
import xlsxwriter


res = pd.read_excel('liveServicesRepo.xlsx', 'Sheet1')
stats = []

for index, n, c in res.itertuples():
    print(n)
    '''commitMessage.commitsForYear(n, c)'''
    s = commitMsgsAnalysis.appStats(n)
    if(s is not None):
        stats.append(s)
        
    
def writeToExcel(rec):   
    workbook = xlsxwriter.Workbook('commits/stats.xlsx')
    worksheet = workbook.add_worksheet()
    
    worksheet.write(0, 0, 'app')
    worksheet.write(0, 1, 'Jan')
    worksheet.write(0, 2, 'Feb')
    worksheet.write(0, 3, 'Mar')
    worksheet.write(0, 4, 'Apr')
    worksheet.write(0, 5, 'Merges')
    worksheet.write(0, 6, 'Commits')
    worksheet.write(0, 7, 'Tri')
    
    c = 1
    for rec in stats:
        (app, table, merges, totalCommits, bi, tri) = rec
        worksheet.write(c, 0, app)
        
        for rec in table.itertuples():
            month, count = rec
            worksheet.write(c, month, count)    
            
        worksheet.write(c, 5, merges)
        worksheet.write(c, 6, totalCommits)
        worksheet.write(c, 7, tri)
        
        c=c+1
        
    workbook.close()

writeToExcel(stats)

