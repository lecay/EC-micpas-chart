#对流潜势预报

import micaps
import datetime
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.font_manager as fm

#filename1 = 'F:/data/micaps/ecmwf_thin/CAPE/999/18051208.006'
#filename2 = 'F:/data/micaps/ecmwf_thin/ki/18051208.006'
filename1 = 'Y:/MICAPS/ecmwf_thin/CAPE/999/19083020.021'
filename2 = 'Y:/MICAPS/ecmwf_thin/ki/19083020.021'
intimestr = '20'+filename1[-12:-4]
dt = int(filename1[-3:])
intime = datetime.datetime.strptime(intimestr, '%Y%m%d%H') #初始场时间
ftime = intime + datetime.timedelta(hours=dt)   #预报场时间
cape = micaps.micaps4(filename1)
ki = micaps.micaps4(filename2)

shpname1 = './shpfiles/bou2_4p.shp'
sr1 = shpreader.Reader(shpname1)
proshp1 = list(sr1.geometries())
shpname2 = './shpfiles/continents_lines.shp'
sr2 = shpreader.Reader(shpname2)
proshp2 = list(sr2.geometries())

fig = plt.figure(figsize=(8.5,6), dpi=150)
ax = plt.axes(projection=ccrs.PlateCarree(), aspect='auto')
ax.add_feature(cfeature.LAKES, alpha=1)
ax.add_geometries(proshp1, ccrs.PlateCarree(), edgecolor='dimgrey', facecolor='none', alpha=1, linewidth=0.5)
ax.add_geometries(proshp2, ccrs.PlateCarree(), edgecolor='dimgrey', facecolor='none', alpha=1, linewidth=0.5)
# ax.set_extent([72, 138, 15, 55], ccrs.PlateCarree())
# ax.set_xticks([80, 90, 100, 110, 120, 130])
# ax.set_yticks([20, 30, 40, 50])
# ax.set_extent([104, 124, 17, 30], ccrs.PlateCarree()) #华南
# ax.set_xticks([105, 110, 115, 120])
# ax.set_yticks([20, 25, 30])
# ax.set_extent([111, 136, 38, 54], ccrs.PlateCarree()) #东北
# ax.set_xticks([115, 120, 125, 130, 135])
# ax.set_yticks([40, 45, 50])
# ax.set_extent([107, 123.5, 33, 42.5], ccrs.PlateCarree()) #华北
# ax.set_xticks([110, 115, 120])
# ax.set_yticks([35, 40])
ax.set_extent([108, 124, 25.5, 35.5], ccrs.PlateCarree()) #华东华中
ax.set_xticks([110, 115, 120])
ax.set_yticks([30, 35])
ax.tick_params(direction='in', pad=2, labelsize=8)
font = fm.FontProperties(fname=r"C:/Windows/Fonts/msyh.ttc")
ax.set_title('EC CAPE(填色)、K指数(等值线)', loc='left', fontproperties=font)
ax.set_title('(+%02dh) %s (CST)' % (dt, ftime.strftime('%Y/%m/%d %H')), loc='right', fontsize=9)
datarange = (cape.endlat, cape.beginlat, cape.beginlon, cape.endlon, ki.endlat, ki.beginlat, ki.beginlon, ki.endlon)
ax.annotate('*数据范围：CAPE %d~%dN %d~%dE | K指数 %d~%dN %d~%dE'% datarange, (0.05,0.02), xycoords='figure fraction', fontproperties=font, fontsize=6, color='grey')


levcape = [100, 500, 1000, 1500, 2000, 3000, 4000]
icmap = colors.ListedColormap(np.loadtxt('./color/GMT_seis.rgb', delimiter=' '))
a = ax.contourf(cape.lon, cape.lat, cape.Z, levcape, extend='max', transform=ccrs.PlateCarree(), cmap=icmap.reversed(), alpha=0.4)
abar = fig.colorbar(a, fraction=0.04, pad=0.02, aspect=50)
abar.ax.tick_params(direction='in', pad=2, labelsize=8)

levki = [32, 35, 40]
b = ax.contour(ki.lon, ki.lat, ki.Z, levki, transform=ccrs.PlateCarree(), colors=['b','r','black'], linewidths=0.8, alpha=0.9)
ax.clabel(b, fmt='%d', inline=True, fontsize=7) 

plt.subplots_adjust(left = 0.05, right = 0.97, bottom = 0.06, top = 0.94,  hspace = 0, wspace = 0)
#plt.savefig('./'+filename1[-12:-4]+'/ts'+filename1[-12:-4]+'.'+filename1[-3:]+'.png')
plt.show()