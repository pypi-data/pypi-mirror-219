from pygeodesy.sphericalNvector import LatLon, perimeterOf, meanOf
from cachetools import cached, FIFOCache
import matplotlib.pyplot as plt, quads
import numpy as np, shapefile, glob
import pandas as pd, os

gltiles = {
    "a10g": [50, 90, -180, -90, 1, 6098, 10800, 4800],
    "b10g": [50, 90, -90, 0, 1, 3940, 10800, 4800],
    "c10g": [50, 90, 0, 90, -30, 4010, 10800, 4800],
    "d10g": [50, 90, 90, 180, 1, 4588, 10800, 4800],
    "e10g": [0, 50, -180, -90, -84, 5443, 10800, 6000],
    "f10g": [0, 50, -90, 0, -40, 6085, 10800, 6000],
    "g10g": [0, 50, 0, 90, -407, 8752, 10800, 6000],
    "h10g": [0, 50, 90, 180, -63, 7491, 10800, 6000],
    "i10g": [-50, 0, -180, -90, 1, 2732, 10800, 6000],
    "j10g": [-50, 0, -90, 0, -127, 6798, 10800, 6000],
    "k10g": [-50, 0, 0, 90, 1, 5825, 10800, 6000],
    "l10g": [-50, 0, 90, 180, 1, 5179, 10800, 6000],
    "m10g": [-90, -50, -180, -90, 1, 4009, 10800, 4800],
    "n10g": [-90, -50, -90, 0, 1, 4743, 10800, 4800],
    "o10g": [-90, -50, 0, 90, 1, 4039, 10800, 4800],
    "p10g": [-90, -50, 90, 180, 1, 4363, 10800, 4800] }


files = [("lake1","/tmp/gshhg-shp-2.3.7/GSHHS_shp/i/GSHHS_i_L2.shp"),
         ("river1","/tmp/gshhg-shp-2.3.7/WDBII_shp/i/WDBII_river_i_L01.shp"),
         ("river2","/tmp/gshhg-shp-2.3.7/WDBII_shp/i/WDBII_river_i_L02.shp"),
         ("river3","/tmp/gshhg-shp-2.3.7/WDBII_shp/i/WDBII_river_i_L03.shp"),
         ("river4","/tmp/gshhg-shp-2.3.7/WDBII_shp/i/WDBII_river_i_L04.shp"),
         ("river5","/tmp/gshhg-shp-2.3.7/WDBII_shp/i/WDBII_river_i_L05.shp"),
         ("river6","/tmp/gshhg-shp-2.3.7/WDBII_shp/i/WDBII_river_i_L06.shp"),
         ("river7","/tmp/gshhg-shp-2.3.7/WDBII_shp/i/WDBII_river_i_L07.shp"),
         ("river8","/tmp/gshhg-shp-2.3.7/WDBII_shp/i/WDBII_river_i_L08.shp"),
         ("river9","/tmp/gshhg-shp-2.3.7/WDBII_shp/i/WDBII_river_i_L09.shp"),
         ("river10","/tmp/gshhg-shp-2.3.7/WDBII_shp/i/WDBII_river_i_L10.shp"),
         ("river11","/tmp/gshhg-shp-2.3.7/WDBII_shp/i/WDBII_river_i_L11.shp")
]

# Datafile is from https://www.ngdc.noaa.gov/mgg/topo/gltiles.html, download
# "all files in on zip", extract zip under /tmp
def preprocess_GLOBE_tile(tile):
    
    x = "/tmp/all10/" + tile
    print (x, os.path.basename(x))
    lat_min, lat_max, lon_min, lon_max, elev_min, elev_max, cols, rows = gltiles[tile]
    print (cols, rows)
    z = np.fromfile(x,dtype='<i2')
    z = np.reshape(z,(round(z.__len__()/cols), cols))

    lon = lon_min + 1/120*np.arange(cols)
    lat = lat_max - 1/120*np.arange(round(z.size/cols))
    downsample = 1
    lat_select = np.arange(0,len(lat),downsample)
    lon_select = np.arange(0,len(lon),downsample)

    zm = z[np.ix_(lat_select,lon_select)]
    zm[zm<0] = 0
    np.savez_compressed("/tmp/" + tile + '.npz',zm)

def preprocess_GLOBE():
    d = "/tmp/all10/*"
    if len(glob.glob(d)) == 0: raise ValueError(d + " does not exist")
    for x in glob.glob(d):
        if os.path.basename(x) in gltiles: 
            print (x, os.path.basename(x))
            preprocess_GLOBE_tile(os.path.basename(x))

def preprocess_GSHHS():         # 
    
    res = []
    for type,file in files:
        print (file)
        sf = shapefile.Reader(file)
        r = sf.records()
        waters = sf.shapes()
        print (len(waters))
        for idx in range(len(waters)):
            water = waters[idx]
            name = r[idx]
            print (name,len(water.parts))
            bounds = list(water.parts) + [len(water.points)]
            for (previous, current) in zip(bounds, bounds[1:]):
                geo = [[x[1],x[0]] for x in water.points[previous:current]]
                if len(geo) < 1: continue
                latlons = [LatLon(a[0],a[1]) for a in geo]
                per = np.round(perimeterOf(latlons, radius=6371),2)
                mid = meanOf(latlons)
                res.append([mid.lat,mid.lon,per,type,geo])

    df = pd.DataFrame(res)
    df.columns = ['lat','lon','perimeter','type','polygon']
    df.to_csv('/tmp/lake_river.csv',index=None)
    
def initialize_kernel(size , sigma): 
    w, h = size                                                  
    x = np.linspace(-1,1,w)                         
    y = np.linspace(-1,1, h)                         
    x_cor, y_cor  = np.meshgrid(x, y) 
    kernel = 1/(2*np.pi*np.power(sigma,2) )*\
             np.exp((- (x_cor ** 2 + y_cor ** 2) )/ 
             (2*np.power(sigma,2)))

    kernel = kernel/np.sum(kernel) # normalization
    print(kernel)
    return kernel

def padding(image):
    padded_image = np.pad(image , ((1,1),(1,1)) , 'constant',
                   constant_values=(0,0) ) 
    return padded_image

def conv2d(image, ftr):                           
    s = ftr.shape + tuple(np.subtract(image.shape, ftr.shape) + 1)
    sub_image = np.lib.stride_tricks.as_strided(image, shape = s,
                strides = image.strides * 2)
    return np.einsum('ij,ijkl->kl', ftr, sub_image)
    
def cdist(p1,p2):    
    distances = np.linalg.norm(p1 - p2, axis=1)
    return distances


def find_tile(lat,lon):
    res = [lat >= x[0] and lon < x[1] and lon >= x[2] and lon < x[3] for x in gltiles.values()]
    return res.index(True)

def test1():
    x = np.array(list(range(4,10)))
    y = np.array(list(range(10,16)))
    z = np.array(list(range(20,26)))
    q = QuadTreeInterpolator(x,y,z)
    for x in q.tree.nearest_neighbors((15,20), count=4):
        print (x)    

def test2():
    q = get_quad(tuple([40]),tuple([30]),'g10g',data_dir=".")
    res = q.interpolate(30.5,40.5)
    print (res)
    res = q.interpolate(30.1,40.1)
    print (res)    

def test3():
    q = get_quad(tuple([-29]),tuple([151]),'l10g',data_dir=".")
    print (q.interpolate(151.20361804339458,-29.35574897873761))
                   
if __name__ == "__main__": 
    
    #preprocess_GSHHS()
    preprocess_GLOBE()
    #test1()
    #test2()
    #test3()
 
