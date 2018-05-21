# -*- coding: utf-8 -*-
"""
Line bot push message test

@author: Bryson Xue

@Note:
	1. $ pip install line-bot-sdk

@Ref:
	https://medium.com/@lukehong/%E5%88%9D%E6%AC%A1%E5%98%97%E8%A9%A6-line-bot-sdk-eaa4abbe8d6e
"""
from linebot import LineBotApi
from linebot.models import TextSendMessage

line_bot_api = LineBotApi('Your Channel Access Token')

#push message to one user
line_bot_api.push_message('user_id', 
	TextSendMessage(text='Hello World!'))

#push message to multiple users
line_bot_api.multicast(['user_id'], 
	TextSendMessage(text='Hello World222!'))