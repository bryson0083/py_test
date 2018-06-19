# -*- coding: utf-8 -*-
"""
Line bot push message test

@author: Bryson Xue

@Note:
	1. $ pip install line-bot-sdk

@Ref:
	https://www.pixpo.net/technology/0I7Qaawp.html
	https://blog.gtwang.org/programming/python-md5-sha-hash-functions-tutorial-examples/
	https://stackoverflow.com/questions/7585307/how-to-correct-typeerror-unicode-objects-must-be-encoded-before-hashing
"""
import hashlib

a = "I am huoty".encode('utf-8')

print(hashlib.md5(a).hexdigest())
print(hashlib.sha1(a).hexdigest())
print(hashlib.sha224(a).hexdigest())
print(hashlib.sha256(a).hexdigest())
print(hashlib.sha384(a).hexdigest())
print(hashlib.sha512(a).hexdigest())