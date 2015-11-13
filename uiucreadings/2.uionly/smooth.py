#!/usr/bin/env python3
import csv
from collections import defaultdict, deque

data = [row for row in csv.reader(open('./uidata.csv'))]
header, data = data[0], data[1:]

# In [3]: rows[0]
# Out[3]: ['id', 'time', 'lat', 'lon', 'bssid', 'ssid', 'level', 'speed', 'accuracy']
# compress data down into single values for each lat/lon

data_map = defaultdict(deque)
for row in data:
    data_map[row[1]].append(row)

compressed_map = deque()
for timechunk, values in data_map.items():
    s, n = 0, 0
    for val in values:
        s += abs(float(val[6]))
        n += 1

    avg = 1 * (s / n)
    ls = [val[2], val[3], avg]
    compressed_map.append(ls)

writer = csv.writer(open('./mapable.csv', 'w'), delimiter=' ')
#writer.writerow(['lat', 'lon', 'mDB'])
for row in compressed_map:
    writer.writerow(row)
