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
output = talib.SMA(close)
print(output)


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.plot(output)
plt.show()


upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)
output = talib.MOM(close, timeperiod=5)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.plot(output)
plt.show()


