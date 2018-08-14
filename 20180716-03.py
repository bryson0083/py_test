"""

Ref:
	https://www.geeksforgeeks.org/python-plotting-google-map-using-gmplot-package/
	https://stackoverflow.com/questions/46833218/python-gmplot-has-no-attitribute-googlemapplotter

"""
from gmplot import gmplot

# Place map
#gmap = gmplot.GoogleMapPlotter(22.56481191, 120.3538521, 13)


# Scatter points
#top_attraction_lats, top_attraction_lons = zip(*[
#    (22.56481191, 120.3538521),
#    (22.57011232, 120.3421469)
#    ])
#gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=80, marker=True)
#latitudes = [22.56481191, ]
#longitudes = [120.3538521, ]
#gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=40)
#gmap = gmplot.GoogleMapPlotter.from_geocode( "Dehradun, India" )

latitude_list = [ 30.3358376, 30.307977, 30.3216419 ]
longitude_list = [ 77.8701919, 78.048457, 78.0413095 ]
 
gmap = gmplot.GoogleMapPlotter(30.3164945,
                                78.03219179999999, 13)
 
# scatter method of map object 
# scatter points on the google map
gmap.scatter( latitude_list, longitude_list, '#FF0000',
                              size = 40, marker = False )
 
# Plot method Draw a line in
# between given coordinates
gmap.plot(latitude_list, longitude_list, 
           'cornflowerblue', edge_width = 2.5)


# Draw
gmap.draw("my_map2.html")
