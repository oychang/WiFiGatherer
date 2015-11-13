#!/usr/bin/env python2
import geoplotlib
from geoplotlib.utils import read_csv, BoundingBox, DataAccessObject

data = read_csv('filtered_lonlat.csv')

# http://andreacuttone.com/geoplotlib/api.html#module-geoplotlib
geoplotlib.dot(data, color=[0,0,0], point_size=1.5)
geoplotlib.kde(data, bw=10, cmap='PuBuGn', cut_below=1e-4, clip_above=1e-2, alpha=180)
geoplotlib.graph(read_csv('group0.csvgraph.csv'), src_lat='flat', src_lon='flon',
        dest_lat='tlat', dest_lon='tlon', color=[0,0,0], linewidth=2)
geoplotlib.graph(read_csv('group1.csvgraph.csv'), src_lat='flat', src_lon='flon',
        dest_lat='tlat', dest_lon='tlon', color=[0,255,0], linewidth=2)
geoplotlib.graph(read_csv('group2.csvgraph.csv'), src_lat='flat', src_lon='flon',
        dest_lat='tlat', dest_lon='tlon', color=[128,0,128], linewidth=2)
geoplotlib.kde(read_csv('chokepoints.csv'), bw=10, cmap='hot',
        cut_below=1e-4, clip_above=1e-2, alpha=180)

bbox = BoundingBox(north=25.7188,west=-80.280,south=25.711,east=-80.280)
geoplotlib.set_bbox(bbox)
geoplotlib.set_window_size(1400, 1600)
#geoplotlib.set_window_size(700, 800)
geoplotlib.tiles_provider('toner')
geoplotlib.set_smoothing(True)
geoplotlib.savefig('output')
#geoplotlib.show()
