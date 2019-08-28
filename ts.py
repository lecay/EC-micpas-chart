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
#filename1 = 'Y:/MICAPS/ecmwf_thin/CAPE/999/19082620.018'
filename2 = 'F:/data/micaps/ecmwf_thin/ki/18051208.006'
cape = micaps.micaps4(filename1)
ki = micaps.micaps4(filename1)

shpname1 = './shpfiles/bou2_4p.shp'
sr1 = shpreader.Reader(shpname1)
proshp1 = list(sr1.geometries())
shpname2 = './shpfiles/continents_lines.shp'
sr2 = shpreader.Reader(shpname2)
proshp2 = list(sr2.geometries())

fig = plt.figure(figsize=(8.5,6), dpi=150)
ax = plt.axes(projection=ccrs.PlateCarree(), aspect='auto')
ax.add_feature(cfeature.LAKES, alpha=1)
ax.add_geometries(proshp1, ccrs.PlateCarree(), edgecolor='grey', facecolor='none', alpha=1, linewidth=0.5)
ax.add_geometries(proshp2, ccrs.PlateCarree(), edgecolor='grey', facecolor='none', alpha=1, linewidth=0.5)
ax.set_extent([72, 138, 15, 55], ccrs.PlateCarree())
ax.set_xticks([80, 90, 100, 110, 120, 130])
ax.set_yticks([20, 30, 40, 50])
ax.set_title('TS')

levcape = [100, 500, 1000, 1500, 2000, 2500, 3000, 4000]
icmap = colors.ListedColormap(np.loadtxt('./color/GMT_seis.rgb', delimiter=' '))
a = ax.contourf(cape.lon, cape.lat, cape.Z, levcape, extend='max', transform=ccrs.PlateCarree(), cmap=icmap.reversed(), alpha=0.4)
fig.colorbar(a, fraction=0.04, pad=0.02, aspect=50)

levki = [32, 35, 40]
b = ax.contour(ki.lon, ki.lat, ki.Z, levki, transform=ccrs.PlateCarree(), colors='red', linewidths=0.5)
ax.clabel(b, fmt='%d', inline=True, fontsize=7) 

plt.show()