import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
from scipy.ndimage.filters import maximum_filter, minimum_filter
import numpy as np

def drawcnmap(ax):    #画带中国省界的地图
	shpname1 = './shpfiles/bou2_4p.shp'
	sr1 = shpreader.Reader(shpname1)
	proshp1 = list(sr1.geometries())
	shpname2 = './shpfiles/continents_lines.shp'
	sr2 = shpreader.Reader(shpname2)
	proshp2 = list(sr2.geometries())
	ax.add_geometries(proshp1, ccrs.PlateCarree(), edgecolor='dimgrey', facecolor='none', alpha=1, linewidth=0.5)
	ax.add_geometries(proshp2, ccrs.PlateCarree(), edgecolor='dimgrey', facecolor='none', alpha=1, linewidth=0.5)

#https://unidata.github.io/python-gallery/examples/HILO_Symbol_Plot.html#sphx-glr-examples-hilo-symbol-plot-py
#标注高低压中心
def plot_maxmin_points(ax, lon, lat, data, extrema, nsize, symbol, color='k',
                       hlsize=19, numsize=8, plotValue=True, transform=None):

    if (extrema == 'max'):
        data_ext = maximum_filter(data, nsize, mode='nearest')
    elif (extrema == 'min'):
        data_ext = minimum_filter(data, nsize, mode='nearest')
    else:
        raise ValueError('Value for hilo must be either max or min')

    mxy, mxx = np.where(data_ext == data)

    for i in range(len(mxy)):
        ax.text(lon[mxy[i], mxx[i]], lat[mxy[i], mxx[i]], symbol, color=color, size=hlsize,
                clip_on=True, horizontalalignment='center', verticalalignment='center',
                transform=transform)
        ax.text(lon[mxy[i], mxx[i]], lat[mxy[i], mxx[i]],
                '\n' + str(np.int(data[mxy[i], mxx[i]])),
                color=color, size=numsize, clip_on=True, fontweight='bold',
                horizontalalignment='center', verticalalignment='top', transform=transform)