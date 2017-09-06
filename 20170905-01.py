import cv2
import requests
import numpy
import PIL
from PIL import Image
from matplotlib import pyplot as plt

with open('kaptcha.jpg', 'wb') as f:
    res = requests.get('http://gcis.nat.gov.tw/pub/kaptcha.jpg')
    f.write(res.content)

image = Image.open('kaptcha.jpg')
#image.show()

pil_image = PIL.Image.open('kaptcha.jpg').convert('RGB')
open_cv_image = numpy.array(pil_image)
#pil_image.show()
#print(open_cv_image)
#plt.imshow(open_cv_image)

imgray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x:x[1])

ary = []
for (c,_) in cnts:
    (x,y,w,h) = cv2.boundingRect(c)
    print((x,y,w,h))
    if w>= 14 and h == 24:
        ary.append((x,y,w,h))

print(ary)