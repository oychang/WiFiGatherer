#!/usr/bin/env python3
import csv

rows = ['id', 'unixms', 'lat', 'lon', 'bssid', 'ssid', 'level', 'speed',
        'accuracy', 'bearing']

with open('filtered.csv') as f:
    data = [row for row in csv.reader(f)]

# find no of unique ap
#unique_aps = set([row[rows.index('bssid')] for row in data])
#print(len(unique_aps))
