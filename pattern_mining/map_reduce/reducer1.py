#!/usr/bin/env python3
"""reducer1.py"""

import sys
lno = 0
su=0
dic={}
prev=""
min_support=2

for line in sys.stdin:
    line = line.strip()
    pattern,support=line.split("\t")
    if(lno!=0):
        if(pattern!=prev):
            if(su>=min_support):
                print('%s\t%s %s' % (1,prev,su))
            su=0
    su+=int(support)
    prev=pattern
    lno+=1

if(lno>0 and su>=min_support):
    print('%s\t%s %s' % (1,prev,su))


    
