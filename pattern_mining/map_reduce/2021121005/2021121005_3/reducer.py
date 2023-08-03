#!/usr/bin/env python3
"""reducer.py"""

from operator import itemgetter
import sys
s=0
i=0
for line in sys.stdin:
    line = line.strip()
    index, elements = line.split('\t', 1)
    elements=int(elements)
    # print(elements)
    s+=elements
    i+=1
print(s/i)

