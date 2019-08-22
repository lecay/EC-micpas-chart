import micaps
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt

filename = 'F:/data/micaps/ecmwf_thin/RH/850/18051208.000'
slp = micaps.micaps4(filename)
slp.readdata
lat = np.arange(slp.beginlat, slp.endlat + slp.deltalat, slp.deltalat)
lon = np.arange(slp.beginlon, slp.endlon + slp.deltalon, slp.deltalon)
lons, lats = np.meshgrid(lon, lat)

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
ax.set_title('RH')

cm = [0, 10, 30, 60, 70, 80, 90, 100]
c = ax.contourf(lons, lats, slp.Z, cm, extend='neither', transform=ccrs.PlateCarree(), cmap=plt.cm.jet_r)
fig.colorbar(c, fraction=0.04, pad=0.02, aspect=50)
plt.show()
