#!/usr/bin/env python3
"""reducer.py"""

from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
m, n, p = 0, 0, 0
result = {}
prev = -1
previ=-1
l = []
dic={}

vals={}
def calc_sum(dic):
    s=0
    for i in dic:
        s+=dic[i]
    return s

maxm=-1*float("inf")
maxn=-1*float("inf")
for line in sys.stdin:
    line = line.strip()
    index, elements = line.split('\t', 1)
    i, j = map(int, index.split())

    elements = elements.split()

    elements[1] = int(elements[1])
    elements[2]=int(elements[2])
    maxm=max(maxm,i)
    maxn=max(j,maxn)

    if(prev==-1):
        prev=j
    if(previ==-1):
        previ=i
    if(prev!=j or previ!=i):
        # if(previ==0 and prev==0):
            # print(calc_sum(dic),len(dic))
        st=str(previ)+" "+str(prev)+" "+str(calc_sum(dic))
        # print('%s\t%s'%(1,st))
        vals.update({(previ,prev):calc_sum(dic)})
        dic={}
   
    if(elements[1] in dic):
        # if(i==15):
        #     print(elements[1], elements[2], dic[elements[1]])
        dic[elements[1]]*=elements[2]
    else:
        dic.update({elements[1]:elements[2]})

    prev=j
    previ=i


st=str(i)+" "+str(j)+" "+str(calc_sum(dic))
if(len(dic)!=0):
    # print('%s\t%s'%(1,st))
    vals.update({(i,j):calc_sum(dic)})

for i in range(int(maxm)+1):
    for j in range(int(maxn)+1):
        if((i,j) in vals):
            print(vals[(i,j)],end=" ")
    print()



