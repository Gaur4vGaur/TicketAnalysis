#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 22:26:53 2018

@author: gaurav
"""

import pandas as pd

res = pd.read_excel('my1.xlsx', 'Sheet3')

for row in res.head(2).itertuples():
    (index, description, url) = row
    print(description)
    print('--------------------------------------')