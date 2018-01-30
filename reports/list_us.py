
"Print sprint info for US."

import csv

with open('export.csv') as f:
    r = csv.reader(f)
    us = [d for d in r if d[0].startswith('US')]
    for line in us:
        print "%s %s" % tuple(line[:2])
