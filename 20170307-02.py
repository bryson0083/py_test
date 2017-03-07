# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:55:20 2017

@author: bryson0083

json file content
{
    "AAA": {
            "id": "aaa_id",
            "pwd": "aaa_pwd"
    },
    "BBB": {
            "id": "bbb_id",
            "pwd": "bbb_pwd"
    },
    "CCC": {
            "id": "ccc_id",
            "pwd": "ccc_pwd"
    }
}

"""

import json
from pprint import pprint

with open('account_test.json') as data_file:    
    data = json.load(data_file)

#全部讀出來
pprint(data)

#讀取某個欄位
print('\n\nAAA account:')
pprint(data['AAA']['id'])
pprint(data['AAA']['pwd'])

print('\n\nBBB account:')
pprint(data['BBB']['id'])
pprint(data['BBB']['pwd'])

print('\n\nCCC account:')
pprint(data['CCC']['id'])
pprint(data['CCC']['pwd'])

