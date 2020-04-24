import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon

#data=gpd.read_file(r"MODIS_C6_SouthEast_Asia_24h/MODIS_C6_SouthEast_Asia_24h.shp")
csv=pd.read_csv(r"MODIS_C6_SouthEast_Asia_24h.csv")

lon = np.array(csv['longitude'].values)
lat = np.array(csv['latitude'].values)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1,projection=ccrs.PlateCarree())

ax.scatter(lon, lat, marker=".",c="red")

ax.stock_img()
ax.coastlines()

extent = [min(lon),max(lon),min(lat),max(lat)]
ax.set_extent(extent)

plt.show()
