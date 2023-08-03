#!/usr/bin/env python3
"""mapper2.py"""

import sys
import math
lno = 0
vals=[]
def prefix_matcher(string1,string2):
    i=0
    while(i<len(string1) and i<len(string2)):
        if(string1[i]!=string2[i]):
            return i
        i+=1
    return i

for line in sys.stdin:
    line = line.strip()
    sno,sequence=line.split("\t")
    vals.append(sequence)

dic={vals[i]:0 for i in range(len(vals))}

for i in range(len(vals)):
    for j in range(len(vals)):
        ind=0
        while(ind<len(vals[j]) and ind<len(vals[i])):
            if(vals[i][ind]!=vals[j][ind]):
                break
            if(vals[i][:ind+1] not in dic):
                dic.update({vals[i][:ind+1]:1})
            else:
                dic[vals[i][:ind+1]]+=1
            ind+=1

    

for i in dic:
    print('%s\t%s' % (i,int(math.sqrt(dic[i]))))
            
            



            
    
