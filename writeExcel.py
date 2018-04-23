#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 07:09:03 2018

@author: gaurav
"""
import xlsxwriter


# Create a Pandas dataframe from some data.
d = [('long', ('g4s', 'need'), 'no longer work for g4s.'), ('confus', ('bit', 'confusing'), ''), ('expect', ('salary', 'month'), 'This was useless for the purpose I wanted to use it forI have been put on tax code BR and am paying loads of tax despite being within my income allowa'), ('read', ('17/18', 'reduction'), 'i dont understand where you get my income for year 17/18 from nor the reduction on my tax code'), ('tax', ('accurate', 'calculations'), ''), ('act', ('actions', 'every'), ''), ('pay', ('earn', 'enough'), 'My payslip shows I am paying tax when I don t earn enough to pay any tax')]

row = 0
col = 0

workbook = xlsxwriter.Workbook('sample.xlsx')
worksheet = workbook.add_worksheet()

for word, bigram, impSent in d:
    w1, w2 = bigram
    worksheet.write(row, col,     word)
    worksheet.write(row, col + 1, w1 + ' ' + w2)
    worksheet.write(row, col + 2, impSent)
    row += 1
    

# Close the Pandas Excel writer and output the Excel file.
workbook.close()