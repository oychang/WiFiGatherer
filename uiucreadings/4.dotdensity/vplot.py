#!/usr/bin/env python2
import geoplotlib
from geoplotlib.utils import read_csv, BoundingBox


data = read_csv('./network_density.csv')
geoplotlib.voronoi(data, line_color='b', line_width=1)
geoplotlib.set_bbox(BoundingBox.DK)
geoplotlib.show()
