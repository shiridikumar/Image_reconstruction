#!/usr/bin/env python3
"""reducer0.py"""

import sys
pos = 0
two_length_join={"A":["T","G","C"],"T":["A","G","C"],"G":["A","T","C"],"C":["A","G","T"]}
for line in sys.stdin:
    line = line.strip()
    # print(line)
    if(len(line)==0):
        continue
    if(line[-1]==","):
        line=line[:-1]
    _,sequences=line.split("\t")
    print('%s\t%s'%("*",sequences))
    sequences=sequences.split(",")
    
    for sequence in sequences:
        sequence=sequence.split()[1]
        for i in range(len(sequence)):
            print('- %s\t%s %s'%(str(pos).zfill(6),sequence[i],0))
            if(i!=0):
                print('- %s\t%s %s'%(str(pos-1).zfill(6),sequence[i],1))   
            pos+=1
        pos+=1

