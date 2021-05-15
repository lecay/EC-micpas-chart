#天气形势图

import micaps
import datetime
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
#import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.font_manager as fm
from scipy import ndimage
from mapfunc import drawcnmap, plot_maxmin_points

filename1 = 'F:/data/micaps/ecmwf_thin/MSL/999/18051208.006'
filename2 = 'F:/data/micaps/ecmwf_thin/uv/850/18051208.006'
# filename1 = 'Y:/MICAPS/ecmwf_thin/CAPE/999/19090320.021'
# filename2 = 'Y:/MICAPS/ecmwf_thin/ki/19090320.021'
intimestr = '20'+filename1[-12:-4]
dt = int(filename1[-3:])
intime = datetime.datetime.strptime(intimestr, '%Y%m%d%H') #初始场时间
ftime = intime + datetime.timedelta(hours=dt)   #预报场时间
slp = micaps.micaps4(filename1)
uv = micaps.micaps11(filename2)

fig = plt.figure(figsize=(8.5,6), dpi=150)
ax = plt.axes(projection=ccrs.PlateCarree(), aspect='auto')
drawcnmap(ax)
ax.set_extent([72, 138, 15, 55], ccrs.PlateCarree())
ax.set_xticks([80, 90, 100, 110, 120, 130])
ax.set_yticks([20, 30, 40, 50])

ax.tick_params(direction='in', pad=2, labelsize=8)
font = fm.FontProperties(fname=r"C:/Windows/Fonts/msyh.ttc")
ax.set_title('EC 500hPa高度场(填色)、海平面气压场(等值线)、850hPa风场', loc='left', fontproperties=font)
ax.set_title('%s  (+%02dh) %s (CST)' % (intimestr, dt, ftime.strftime('%Y/%m/%d %H')), loc='right', fontsize=9)
# datarange = (cape.endlat, cape.beginlat, cape.beginlon, cape.endlon, ki.endlat, ki.beginlat, ki.beginlon, ki.endlon)
# ax.annotate('*数据范围：CAPE %d~%dN %d~%dE | K指数 %d~%dN %d~%dE'% datarange, (0.05,0.02), xycoords='figure fraction', fontproperties=font, fontsize=6, color='grey')

sta = pd.read_csv('./station.txt', header=None, sep=r'[\s]+', engine='python', names=['name','lon','lat','grade'])
mainsta = sta[sta.grade==1]
ax.plot(mainsta['lon'], mainsta['lat'], marker='.', color='dimgrey', markersize=2, linestyle='', transform=ccrs.PlateCarree())

# levcape = [100, 500, 1000, 1500, 2000, 3000, 4000]
# icmap = colors.ListedColormap(np.loadtxt('./color/GMT_seis.rgb', delimiter=' '))
# a = ax.contourf(cape.lon, cape.lat, cape.Z, levcape, extend='max', transform=ccrs.PlateCarree(), cmap=icmap.reversed(), alpha=0.4)
# abar = fig.colorbar(a, fraction=0.04, pad=0.02, aspect=50)
# abar.ax.tick_params(direction='in', pad=2, labelsize=8)

levslp = list(range(900,1100,2))
slps = ndimage.gaussian_filter(slp.Z, sigma=4, order=0, mode="wrap",truncate = 4.0)
b = ax.contour(slp.lon, slp.lat, slps, levslp, transform=ccrs.PlateCarree(), colors='darkblue', linewidths=0.8, alpha=0.8)
ax.clabel(b, fmt='%d', inline=True, fontsize=7) 
plot_maxmin_points(ax, slp.lon, slp.lat, slps, 'max', 60, symbol='H', color='b',  transform=ccrs.PlateCarree())
plot_maxmin_points(ax, slp.lon, slp.lat, slps, 'min', 60, symbol='L', color='r',  transform=ccrs.PlateCarree())

uvlats = np.arange(uv.beginlat, uv.endlat + uv.deltalat, 1)
uvlons = np.arange(uv.beginlon, uv.endlon + uv.deltalon, 1)
uvlon, uvlat = np.meshgrid(uvlons, uvlats)
ax.barbs(uvlon, uvlat, uv.U, uv.V,length=2, barb_increments=dict(half=2, full=4, flag=20),
          sizes=dict(emptybarb=0.1,spacing=0.17,width=0.3), alpha=0.7)

plt.subplots_adjust(left = 0.05, right = 0.97, bottom = 0.06, top = 0.94,  hspace = 0, wspace = 0)
#plt.savefig('./'+filename1[-12:-4]+'/ts'+filename1[-12:-4]+'.'+filename1[-3:]+'.png')
plt.show()