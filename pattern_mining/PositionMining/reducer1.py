#!/usr/bin/env python3
"""reducer1.py"""

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
    if(key[0]=="*"):
        continue
    position=int(key[1])
    id=int(key[2])
    if(lno!=0):
        if(prev_key==key):
            if(postfix=="-"):
                postfix=""  
            pattern=prefix[0]+postfix+prev_prefix
            # print(pattern)
            if(prev_flag==0):
                pattern=prev_prefix+postfix+prefix[0]
            
            if(pattern not in dic):
                dic.update({pattern:[(position,id)]})

            else:
                dic[pattern].append((position,id))

    lno+=1
    prev_flag=int(prefix[1])
    prev_key=key
    prev_prefix=prefix[0]








for pattern in dic:
    if(len(dic[pattern])>=min_sup):
        for position in dic[pattern]:
            print('%s %s %s\t%s %s'%(pattern[1:],str(position[0]).zfill(6),str(position[1]).zfill(6),pattern[0],0))
            if(position!=0):
                print('%s %s %s\t%s %s'%(pattern[:-1],str(position[0]-1).zfill(6),str(position[1]).zfill(6),pattern[-1],1))

            




