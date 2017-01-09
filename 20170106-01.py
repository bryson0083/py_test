# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 09:16:46 2017

@author: bryson0083
"""

import csv

with open('test.csv', 'r') as f:
  reader = csv.reader(f)
  your_list = list(reader)

print(your_list)