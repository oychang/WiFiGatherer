# coding: utf-8
runs = [0 for x in named_data]
for i, x in enumerate(named_data):
    if i > 0:
        if named_data[i-1].lat != x.lat or named_data[i-1].lon != x.lon:
            runs[i] = 1

export = tmp3.gen(runs, named_data)
header = ['lat', 'lon', 'ap']
with open('network_density.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for x in export:
        writer.writerow(x)

