#!/usr/bin/env python3
"""reducer2.py"""

import sys
lno = 0
prev_key=""
prev_flag=-1
prev_prefix=""
new_patterns=[]
dic={}
min_sup=2
support={}
for line in sys.stdin:
    line = line.strip()
    key,prefix=line.split("\t")
    prefix=prefix.split()
    key=key.split()
    postfix=key[0]
    position=int(key[1])
    id=int(key[2])
    if(int(prefix[1])==0):
        pattern=prefix[0]+postfix
        print('%s\t id : %s , position : %s'%(pattern,id,position))


