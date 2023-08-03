#!/usr/bin/env python3
"""mapper.py"""

import sys
lno = 0
matrices = []
m1 = 0
m2 = 0
m = 0
n = 0
p = 0
mat1 = []
mat2 = []
inp = []
for line in sys.stdin:
    line = line.strip()
    line = list(map(int, line.split()))
    if(line[-1] == 0):
        for i in range(line[1]):
            it = "A "+str(line[3])+" "+str(line[4])
            st = str(line[2]).zfill(4)+" "+str(i).zfill(4)
            print('%s\t%s' % (st, it))
    else:
        for i in range(line[0]):
            it = "B "+str(line[2])+" "+str(line[4])
            st = str(i).zfill(4)+" "+str(line[3]).zfill(4)
            # if(i==82):
            print('%s\t%s' % (st, it))
