# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 11:55:12 2017

@author: bryson0083
"""
import os

def test_a():
	print("call from a")
	print(os.path.basename(__file__))
	#print(__file__)
	#print(__name__)

if __name__ == '__main__':
	test_a()