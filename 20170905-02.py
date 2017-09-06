# -*- coding: utf-8 -*-
"""
類神經網路機器學習~辨識驗證碼
(經濟部─公司及分公司基本資料查詢)

@author: Bryson Xue
@target_rul: 
    查詢網頁 => http://gcis.nat.gov.tw/pub/cmpy/cmpyInfoListAction.do
@Note: 
    1. activate ENV => $ activate opencvtest
    2. 需要檔案captcha.pkl
    3. 事先建立目錄imagedata，存放處理完的圖片
"""
import requests
import numpy
import PIL
import cv2
import time
import os
from matplotlib import pyplot as plt
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from PIL import Image

def saveKaptcha(image, dest):
    scaler = StandardScaler()
    pil_image = PIL.Image.open(image).convert('RGB') 
    open_cv_image = numpy.array(pil_image) 
    imgray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x:x[1])
    ary = []
    for (c,_) in cnts:
        (x,y,w,h) = cv2.boundingRect(c)
        if w>= 14 and h == 24:
            if w >= 20:
                w1 = int(w / 2)
                ary.append((x,y,w1,h))
                ary.append((x+w1,y,w1,h))
            else:
                ary.append((x,y,w,h))
                
    data = []
    for idx, (x,y,w,h) in enumerate(ary):
        fig = plt.figure()
        roi = open_cv_image[y:y+h, x:x+w]
        thresh = roi.copy()
        plt.imshow(thresh)
        plt.savefig(os.path.join(dest, '{}.jpg'.format(idx)), dpi=100)

def predictKaptcha(dest):
    data = []
    for idx, img in enumerate(os.listdir(dest)):
        pil_image = PIL.Image.open(os.path.join(dest,'{}'.format(img))).convert('1') 
        wpercent = (basewidth/float(pil_image.size[0]))
        #hsize = int((float(pil_image.size[1])*float(wpercent)))
        hsize = 33
        img = pil_image.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        data.append([pixel for pixel in iter(img.getdata())])
    scaler.fit(data)
    data_scaled = scaler.transform(data)
    return clf.predict(data_scaled)

########################################################################
# MAIN
########################################################################
clf = joblib.load('captcha.pkl')
scaler = StandardScaler()
basewidth = 50

rs  = requests.session()
res = rs.get('http://gcis.nat.gov.tw/pub/cmpy/cmpyInfoListAction.do')
with open('kaptcha.jpg', 'wb') as f:
    res2 = rs.get('http://gcis.nat.gov.tw/pub/kaptcha.jpg')
    f.write(res2.content)

saveKaptcha('kaptcha.jpg', 'imagedata') 
kaptcha = predictKaptcha('imagedata')

print(kaptcha)
image = Image.open('kaptcha.jpg')
image.show()