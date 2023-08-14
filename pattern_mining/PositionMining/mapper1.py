#!/usr/bin/env python3
"""mapper1.py"""
import sys
pos = 0
two_length_join={"A":["T","G","C"],"T":["A","G","C"],"G":["A","T","C"],"C":["A","G","T"]}
string=""
for line in sys.stdin:
    line=line.strip()
    line=line.split(",")
    id,sequence=line[0],line[1]
    for i in range(len(sequence)):

        print('- %s %s\t%s %s'%(str(i).zfill(6),str(id).zfill(6),sequence[i],0))
        if(i!=0):
            print('- %s %s\t%s %s'%(str(i-1).zfill(6),str(id).zfill(6),sequence[i],1))   
    # pos+=1
    # print('%s\t%s'%("-",string))



    # line = line.strip()
    # if(line[-1]==","):
    #     line=line[:-1]
    # id,sequence=line.split(",")
    # for i in range(len(sequence)):
    #     print('-\t%s %s %s'%(pos,sequence[i],0))
    #     if(i!=0):
    #         print('-\t%s %s %s'%(pos-1,sequence[i],1))
    #     pos+=1
    # pos+=1
    


