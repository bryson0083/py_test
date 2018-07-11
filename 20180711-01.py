# encoding: utf-8
"""
import 自行開發程式

建置測試目錄
[util]  ---> [Core_a] ---> fun_core_a.py
        ---> [Core_b] ---> fun_core_b.py

Note:
	作為放置自製lib的每個目錄，需放置 __init__.py 的檔案

"""
#import方式1
#from util.Core_a.fun_core_a import fun_core_a1
from util.Core_b.fun_core_b import fun_core_b1, fun_core_b2

#import方式2
import util.Core_a.fun_core_a as alias_a

a = alias_a.fun_core_a2()
print(a)

ab = alias_a.fun_core_ab()
print(ab)

b1 = fun_core_b1()
print(b1)

b2 = fun_core_b2()
print(b2)