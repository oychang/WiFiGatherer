#!/usr/bin/env python3
# coding: utf-8

from sys import argv
from collections import defaultdict, deque, namedtuple
import csv

if len(argv) < 2:
    print('usage: ./density.py <out.csv>')
    raise SystemExit(1)

with open(argv[1]) as f:
    reader = csv.reader(f)
    data = [row for row in reader]

header, data = data[0], data[1:]
header[0] = header[0][1:]
Reading = namedtuple('Reading', header)
data = (Reading(*row) for row in data)

data_by_loc = defaultdict(deque)
for row in data:
    key = row.lat + row.lon
    data_by_loc[key].append(row) # readings for that loc, not unique bssid!

data_for_export = deque()
ui_data_for_export = deque()
whitelist = frozenset(('IllinoisNet', 'UIUCnet', 'UIpublicWiFi', 'eduroam'))
for value in data_by_loc.values():
    ls = (value[0].lat, value[0].lon, len(value))
    data_for_export.append(ls)

    value = [x for x in value if x.ssid in whitelist]
    if len(value) > 0:
        ls = (value[0].lat, value[0].lon, len(value))
        ui_data_for_export.append(ls)

header = ('lat', 'lon', 'apcount')
with open('network_density.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for x in data_for_export:
        writer.writerow(x)

with open('ui_network_density.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for x in ui_data_for_export:
        writer.writerow(x)
