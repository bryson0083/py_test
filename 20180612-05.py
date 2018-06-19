# -*- coding: utf-8 -*-  
"""
matplotlib全域字體參數設定

Ref:
	https://blog.csdn.net/ass7798/article/details/79087312

"""
import matplotlib.pyplot as plt  
from pylab import mpl  
mpl.rcParams['font.sans-serif'] = ['Microsoft JhengHei']   # 微軟正黑體

plt.xlabel(u"哈哈")  
plt.ylabel(u"哈哈")  
plt.title(u"哈哈")  

plt.show()