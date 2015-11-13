#!/usr/bin/env python3
import csv
from glob import glob

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

# do connectivity analysis
for fn in glob('group?.csv'):
    with open(fn) as f:
        gdata = [row for row in csv.reader(f)]
    tindex = rows.index('unixms')
    bindex = rows.index('bssid')
    bssids_by_time = []
    last_time = gdata[0][tindex]
    last_time_bssids = set()
    for row in gdata:
        if row[tindex] != last_time:
            bssids_by_time.append(last_time_bssids)
            last_time_bssids = set()
            last_time = row[tindex]
        last_time_bssids.add(row[bindex])
    print('{} {}'.format(len(bssids_by_time), fn))
    # do max speed analysis
    #print(max([float(row[rows.index('speed')]) for row in gdata]))

    flow = 0
    for i, period in enumerate(bssids_by_time[1:]):
        if len(bssids_by_time[i-1] & period) == 0:
            print('failed intersection at {}'.format(flow))
            flow = 0
        else:
            flow += 1