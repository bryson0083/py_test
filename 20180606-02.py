# -*- coding: utf-8 -*-
"""
base64可還原式編碼

@author: Bryson Xue

@Note:

@Ref:
	https://stackoverflow.com/questions/33054527/python-3-5-typeerror-a-bytes-like-object-is-required-not-str-when-writing-t
	http://jhjguxin.herokuapp.com/2012/04/410/
	https://blog.csdn.net/lxdcyh/article/details/4021476
		Base64编码是一种“防君子不防小人”的编码方式。广泛应用于MIME协议，作为电子邮件的传输编码，生成的编码可逆，后一两位可能有“=”，生成的编码都是ascii字符。
		优点：速度快，ascii字符，肉眼不可理解
		缺点：编码比较长，非常容易被破解，仅适用于加密非关键信息的场合

"""
import base64

str_a = 'yu63158'.encode('utf-8')
encoded = base64.b64encode(str_a)
print(encoded)
decoded = base64.b64decode(encoded)
print(decoded)