
"Print defects."

import csv

with open('export.csv') as f:
    r = csv.reader(f)
    defects = [d for d in r if d[0].startswith('DE')]
    accepted = (a for a in defects if a[2].startswith('Accept'))
    completed = (c for c in defects if c[2].startswith('Complete'))
    for line in accepted:
        print "%s %s" % tuple(line[:2])
    print
    for line in completed:
        print "%s %s" % tuple(line[:2])
