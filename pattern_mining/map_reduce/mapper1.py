#!/usr/bin/env python3
"""mapper1.py"""

import sys
lno = 0
for line in sys.stdin:
    line = line.strip()
    id,sequence=line.split(",")
    for i in range(len(sequence)):
        if(i!=len(sequence)-1):
            print('%s\t%s' % (lno, sequence[i:]))
            lno+=1
