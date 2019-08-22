import codecs
import re
import numpy as np
#import math
#from scipy.interpolate import Rbf
from scipy import interpolate

def interp(lon,beginlon,deltalon,lat,beginlat,deltalat,va):  #插值方法
    lx = int((lon-beginlon)/deltalon)*deltalon + beginlon
    ly = int((lat-beginlat)/deltalat)*deltalat + beginlat
    lX = np.array([[lx,lx+deltalon],[lx,lx+deltalon]])  #临近4点坐标
    lY = np.array([[ly,ly],[ly+deltalat,ly+deltalat]])
    lj = ((lX-beginlon)/deltalon).astype(int)
    li = ((lY-beginlat)/deltalat).astype(int)
    lU = np.array([[va[li[0,0],lj[0,0]],va[li[0,1],lj[0,1]]],[va[li[1,0],lj[1,0]],va[li[1,1],lj[1,1]]]])
    fU = interpolate.interp2d(lX, lY, lU, kind='linear')
    #fU = Rbf(rlX, rlY, lU, fraction='linear')
    nv = fU(lon, lat)
    #print(lU)
    return nv

class micaps4(object):
    def __init__(self, filename):
        self.filename = filename
        f = codecs.open(self.filename ,mode='r', encoding='GBK')
        text = f.read().strip()
        f.close()
        data = re.split('[\s]+', text)
        begin = 22
        self.yy = int(data[3])
        self.mm = int(data[4])
        self.dd = int(data[5])
        self.hh = int(data[6])   #时次
        self.forehh = int(data[7])  #时效
        self.lev = data[8].strip()  #层次  
        self.deltalon = float(data[9])   #经度格距
        self.deltalat = float(data[10])   #纬度格距
        self.beginlon = float(data[11])   #起始经度
        self.endlon = float(data[12])   #终止经度
        self.beginlat = float(data[13])   #起始纬度
        self.endlat = float(data[14])    #终止纬度
        self.sumlon = int(data[15])   #纬向格点数
        self.sumlat = int(data[16])   #经向格点数
        self.Z = np.zeros((self.sumlat, self.sumlon))
        for i in range(self.sumlat):
            for j in range(self.sumlon):
                self.Z[i, j] = float(data[begin + i * self.sumlon + j])

        lats = np.arange(self.beginlat, self.endlat + self.deltalat, self.deltalat)
        lons = np.arange(self.beginlon, self.endlon + self.deltalon, self.deltalon)
        self.lon, self.lat = np.meshgrid(lons, lats)    #生成数据范围的经纬度矩阵

class micaps11(object):
    def __init__(self, filename):
        self.filename = filename
        f = codecs.open(self.filename ,mode='r', encoding='GBK')
        text = f.read().strip()
        f.close()
        data = re.split('[\s]+', text)
        begin = 17
        self.yy = int(data[3])
        self.mm = int(data[4])
        self.dd = int(data[5])
        self.hh = int(data[6])   #时次
        self.forehh = int(data[7])  #时效
        self.lev = data[8].strip()  #层次  
        self.deltalon = float(data[9])   #经度格距
        self.deltalat = float(data[10])   #纬度格距
        self.beginlon = float(data[11])   #起始经度
        self.endlon = float(data[12])   #终止经度
        self.beginlat = float(data[13])   #起始纬度
        self.endlat = float(data[14])    #终止纬度
        self.sumlon = int(data[15])   #纬向格点数
        self.sumlat = int(data[16])   #经向格点数
        # x = np.arange(beginlon, endlon + deltalon, deltalon)
        # y = np.arange(beginlat, endlat + deltalat, deltalat)
        # X, Y = np.meshgrid(x, y)
        self.U = np.zeros((self.sumlat, self.sumlon))
        self.V = np.zeros((self.sumlat, self.sumlon))
        #Z = np.zeros((sumlat, sumlon))   
        for i in range(self.sumlat):
            for j in range(self.sumlon):
                self.U[i, j] = float(data[begin + i * self.sumlon + j])

        vbegin = begin + self.sumlat * self.sumlon
        for i in range(self.sumlat):
            for j in range(self.sumlon):
                self.V[i, j] = float(data[vbegin + i * self.sumlon + j])

        lats = np.arange(self.beginlat, self.endlat + self.deltalat, self.deltalat)
        lons = np.arange(self.beginlon, self.endlon + self.deltalon, self.deltalon)
        self.lon, self.lat = np.meshgrid(lons, lats)
        # for i in range(sumlon):
        #     for j in range(sumlat):
        #         Z[i, j] = math.sqrt(U[j, i] ** 2 + V[j, i] ** 2)
