"""

Ref:
    https://stackoverflow.com/questions/19726663/how-to-save-the-pandas-dataframe-series-data-as-a-figure
    http://matplotlib.1069221.n5.nabble.com/Draw-only-table-without-XY-Axis-td19546.html


    https://blog.csdn.net/ass7798/article/details/79087312

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):

    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax

def table_to_image(arg_df, img_name):
    df = pd.DataFrame()
    df = arg_df
    #df['日期'] = ['2016-04-01', '2016-04-02', '2016-04-03']
    #df['calories'] = [2200, 2100, 1500]
    #df['sleep hours'] = [2200, 2100, 1500]
    #df['gym'] = [True, False, False]

    render_mpl_table(df, header_columns=0, col_width=2.0)
    plt.savefig('test22222.png')

if __name__ == "__main__":
    print('請勿直接執行本程式...')