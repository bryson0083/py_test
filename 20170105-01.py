# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 08:58:35 2017

@author: bryson0083
"""

name = "aaa.csv"
file = open(name,"a",encoding="big5")

file.write("測試資料")

file.close()