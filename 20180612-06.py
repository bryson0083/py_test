# -*- coding: utf-8 -*-  
"""
matplotlib個別指定字體參數

Ref:
	https://blog.csdn.net/ass7798/article/details/79087312

"""
import matplotlib.pyplot as plt  
from matplotlib.font_manager import FontProperties 

#字型檔指定絕對路徑
#font = FontProperties(fname=r"D:\py_test\Microsoft JhengHei.ttf", size=14)  

#字型檔放置同一層目錄
font = FontProperties(fname=r"Microsoft JhengHei.ttf", size=14)  

plt.xlabel(u"哈哈", fontproperties=font)  
plt.ylabel(u"哈哈", fontproperties=font)  
plt.title(u"哈哈", fontproperties=font)  
plt.show()