# coding: utf-8
import csv
import json
from collections import namedtuple

Reading = namedtuple('Reading', data[0])


data = [row for row in csv.reader(open('run1.csv'))]
data[0][0] = 'id'

Reading = namedtuple('Reading', data[0])
named_data = [Reading(*x) for x in data[1:]]

with open('run1.json', 'w') as f:
    tmp = [x._asdict() for x in named_data]
    json.dump(tmp, f)
