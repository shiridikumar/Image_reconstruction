#!/usr/bin/env python3
"""reducer2.py"""

import sys
lno = 0
su=0
dic={}
prev=""
l=[]

for line in sys.stdin:
    line = line.strip()
    sequence,support=line.split("\t")[1].split()
    if(lno!=0):
        if(len(prev)>len(sequence)):
            l.append((prev,su))
        else:
            if(sequence[:len(prev)]!=prev):
                l.append((prev,su))
    lno+=1
    prev=sequence
    su=support

s=[]
for i in range(len(l)):
    flag=0
    for j in range(len(l)):
        if(i==j):
            continue
        if(l[i][0] in l[j][0]):
            flag=1
            break
    if(flag==0):
        s.append(l[i])


for i in s:
    print('%s\t%s'%(i[0],i[1]))


                


