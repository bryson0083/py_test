import pandas as pd 
from gmplot import gmplot

df = pd.read_csv('red-orange-line-station.csv')
#print(df)

gmap = gmplot.GoogleMapPlotter(22.56481191, 120.3538521, 13)

latitude_list = []
longitude_list = []
for index, row in df.iterrows():
	latitude_list.append(row['車站緯度'])
	longitude_list.append(row['車站經度'])

#print(latitude_list)
#print(longitude_list)

gmap.scatter(latitude_list, longitude_list, '#FF0000', size = 40, marker = False )

# Draw
gmap.draw("my_map2.html")