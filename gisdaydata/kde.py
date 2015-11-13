#!/usr/bin/env python2
import geoplotlib
from geoplotlib.utils import read_csv, BoundingBox, DataAccessObject

data = read_csv('filtered_lonlat.csv')

geoplotlib.dot(data, color=[0,0,0], point_size=1.5)
geoplotlib.kde(data, bw=10, cmap='PuBuGn', cut_below=1e-4, clip_above=.1, alpha=180)
#geoplotlib.kde(data, bw=5, cmap='jet', cut_below=1e-4, scaling='lin')

bbox = BoundingBox(north=25.72,west=-80.28,south=25.71,east=-80.28)
geoplotlib.set_bbox(bbox)
geoplotlib.set_window_size(700, 800)
geoplotlib.show()

