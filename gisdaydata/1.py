#!/usr/bin/env python3
import csv

rows = ['id', 'unixms', 'lat', 'lon', 'bssid', 'ssid', 'level', 'speed',
        'accuracy', 'bearing']

with open('filtered.csv') as f:
    data = [row for row in csv.reader(f)]

# find no of unique ap
#unique_aps = set([row[rows.index('bssid')] for row in data])
#print(len(unique_aps))

# find time split points
#times = set([row[rows.index('unixms')] for row in data])
#times = sorted(list(times))
#deltas = []
#for i, time in enumerate(times[:-1]):
#    ms_delta = int(times[i+1]) - int(time)
#    deltas.append(ms_delta / 1000. / 60)
#print(sorted(deltas)[-5:])

# generate separate csv files for the split points
#N_GROUPS = 3
#groupings = []
#tindex = rows.index('unixms')
#grouping = []
#for i, row in enumerate(data[:-1]):
#    grouping.append(row)
#
#    next_row_time = data[i+1][tindex]
#    delta = int(next_row_time) - int(row[tindex])
#    delta_minutes = delta / 1000. / 60
#    if delta_minutes > 60.0: # some constant from the split point analysis
#        groupings.append(grouping)
#        grouping = []
#else:
#    grouping.append(row[-1])
#    groupings.append(grouping)
#for i, grouping in enumerate(groupings):
#    fn = 'group{}.csv'.format(i)
#    with open(fn, 'w') as f:
#        writer = csv.writer(f)
#        for row in grouping:
#            writer.writerow(row)
