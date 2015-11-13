#!/usr/bin/env python2

import geoplotlib
from geoplotlib.utils import read_csv

data = read_csv('ui_network_density.csv')
geoplotlib.dot(data)
geoplotlib.show()
