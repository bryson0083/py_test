# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:44:12 2017

@author: bryson0083
"""


import numpy
import talib
import matplotlib.pyplot as plt
from talib import MA_Type

close = numpy.random.random(100)
print(close)

#Moving Average
output = talib.SMA(close,30)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.title("MA5 Moving Average")
plt.plot(output)
plt.show()

#Index BBANDS
upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.title("BBANDS")
plt.plot(upper)
plt.plot(middle)
plt.plot(lower)
plt.show()

#Index MOM 
output = talib.MOM(close, timeperiod=5)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.title("Momentum Index")
plt.plot(output)
plt.show()


