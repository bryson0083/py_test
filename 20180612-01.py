"""
Ref:
    https://stackoverflow.com/questions/35634238/how-to-save-a-pandas-dataframe-table-as-a-png/35715029
    https://stackoverflow.com/questions/26678467/export-a-pandas-dataframe-as-a-table-image/26681726
    https://stackoverflow.com/questions/35634238/how-to-save-a-pandas-dataframe-table-as-a-png

"""
import matplotlib

matplotlib.use('Agg')
from matplotlib.pyplot import figure
from matplotlib.table import table
from pylab import *

fig = figure()

colLabels = ('Freeze', 'Wind', 'Flood', 'Quake', 'Hail')
rowLabels = ['%d year' % x for x in (100, 50, 20, 10, 5)]
cellText = [['66.4', '174.3', '75.1', '577.9', '32.0'], ['124.6', '555.4', '153.2', '677.2', '192.5'], ['213.8', '636.0', '305.7', '1175.2', '796.0'], ['292.2', '717.8', '456.4', '1368.5', '865.6'], ['431.5', '1049.4', '799.6', '2149.8', '917.9']]
#table(cellText=cellText, colLabels=colLabels)

ax = subplot(111, frame_on=False) 
ax.xaxis.set_visible(False) 
ax.yaxis.set_visible(False) 

table(cellText=cellText, colLabels=colLabels) 

fig.savefig('test12.png')