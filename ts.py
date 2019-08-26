#对流潜势预报

import micaps
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
from matplotlib import colors
import cmaps

filename1 = 'F:/data/micaps/ecmwf_thin/CAPE/999/18051208.006'
cape = micaps.micaps4(filename1)

shpname1 = './shpfiles/bou2_4p.shp'
a = shpreader.Reader(shpname1)
proshp1 = list(a.geometries())
shpname2 = './shpfiles/continents_lines.shp'
b = shpreader.Reader(shpname2)
proshp2 = list(b.geometries())

fig = plt.figure(figsize=(8.5,6), dpi=150)
ax = plt.axes(projection=ccrs.PlateCarree(), aspect='auto')
ax.add_feature(cfeature.LAKES, alpha=1)
ax.add_geometries(proshp1, ccrs.PlateCarree(), edgecolor='grey', facecolor='none', alpha=1, linewidth=0.5)
ax.add_geometries(proshp2, ccrs.PlateCarree(), edgecolor='grey', facecolor='none', alpha=1, linewidth=0.5)
ax.set_extent([72, 138, 15, 55], ccrs.PlateCarree())
ax.set_xticks([80, 90, 100, 110, 120, 130])
ax.set_yticks([20, 30, 40, 50])
ax.set_title('CAPE')

cm = [100, 500, 1000, 1500, 2000, 2500, 3000, 4000]
rgb = np.loadtxt('./color/cape.rbg', delimiter='\t')
rgb /= 255.0
#icmap = colors.ListedColormap(rgb, name='my_color')
c = ax.contourf(cape.lon, cape.lat, cape.Z, cm, extend='max', transform=ccrs.PlateCarree(), colors=rgb)
#c = ax.contourf(cape.lon, cape.lat, cape.Z, cm, extend='max', transform=ccrs.PlateCarree(), cmap=icmap)
fig.colorbar(c, fraction=0.04, pad=0.02, aspect=50)
plt.show()