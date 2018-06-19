# -*- coding: utf-8 -*-  
from matplotlib.font_manager import FontProperties  
import matplotlib.pyplot as plt  
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)  
plt.xlabel(u"哈哈", fontproperties=font)  
plt.ylabel(u"哈哈", fontproperties=font)  
plt.title(u"哈哈",fontproperties=font)  
plt.show()