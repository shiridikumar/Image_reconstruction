#!/usr/bin/env python3
"""mapper.py"""

import random
import sys
for line in sys.stdin:
    line = line.strip()
    n=int(line)
    # for i in range(n):
    flag=0
    s=0
    turns=0
    while(flag==0):
        a=random.uniform(0,1)
        s+=a
        turns+=1
        if(s>1):
            flag=1
            break
    print('%s\t%s'%(1,turns))





