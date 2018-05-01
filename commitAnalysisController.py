# -*- coding: utf-8 -*-
"""
Created on Tue May  1 15:31:31 2018

@author: gaurav.gaur
"""

import pandas as pd
import xlsxwriter


res = pd.read_excel('C:/1My/study/project/TicketAnalysis/commits/liveServicesRepo.xlsx', 'Sheet1')
for index, n, c in res.itertuples():
    print(n)
    commitsForYear(n, c)