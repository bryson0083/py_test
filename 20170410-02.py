import codecs
from bs4 import BeautifulSoup

f=codecs.open("C:/Users/bryson0083/Desktop/stock105.html", 'r')
#print(f.read())

data = f.read()
#data.encoding = "utf-8"
sp = BeautifulSoup(data, 'html.parser')
#print(sp)

table = sp.findAll('table', attrs={'class':'hasBorder'})

