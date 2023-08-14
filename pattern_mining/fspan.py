import pandas as pd
import numpy as np
import math

__copyright__ = """
 Copyright (C)  2021 Rage Uday Kiran

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class Node:
    def __init__(self,symbol,leaf=False):
        self.val=symbol
        self.children=[]
        self.ischild={i:None for i in range(26)}
        self.leaf=leaf
        self.freq={}
        self.count=1
        self.seq=""




class FSpanMining:
    """
        :Description:  describe the algorithm
        :Reference: provide the reference of the algorithm with URL of the paper, if possible

        :param  inputParameters: parameterType :
                    description of the parameters. Parameters are the variables used in problem definition of the model.

        :Attributes:
            min_IG: float
                minimum threshold for information gain
            
            min_conf: float
                minimum threshold for confidence

            data: numpy 2d array consisting of sequence id's in the first column and and the sequence string in the second column

         **Credits:**
        -------------
             The complete program was written by Shiridi kumar under the supervision of Professor uday rage.

    """

    def __init__(self,minsup,data):
        self.min_sup=minsup
        self.data=data



    def getfreqs(self):
        self.symbol_freq=[0 for i in range(26)]
        self.total_length=0
        for i in range(len(self.data)):
            seq=self.data[i][1]
            for i in seq:
                self.symbol_freq[ord(i)-ord("A")]+=1
            self.total_length+=len(seq)
        self.unique=0
        temp=[]
        for i in range(len(self.symbol_freq)):
            if(self.symbol_freq[i]!=0):
                self.unique+=1
            if(self.symbol_freq[i]>=self.min_sup):
                temp.append(chr(ord("A")+i))
        
        
        return temp

    


    

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns

        :rtype: dict
        """
        return self.frequent

    
    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe

        :rtype: pd.DataFrame
        """

        seqs=[]
        sup=[]
        for i in self.frequent:
            seqs.append(i)
            sup.append(self.frequent[i])


            
        dataFrame =pd.DataFrame()
        dataFrame["Patterns"]=seqs
        dataFrame["Support"]=sup
        return dataFrame


    def save(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file

        :type outFile: file
        """

        self._oFile = outFile
        df=self.getPatternsAsDataFrame()
        df.to_csv(self._oFile)
        
    def FSpanTree(self,prefix,currdb,fixed_length_w=4):
        root=Node(prefix)
        root.count=len(currdb)
        for seq in currdb:
            curr=root
            for i in range(len(seq)):
                if(curr.ischild[ord(seq[i])-ord("A")]):
                    curr.ischild[ord(seq[i])-ord("A")].count+=1

                else:
                    new=Node(seq[i],False)
                    curr.ischild[ord(seq[i])-ord("A")]=new
                    curr.children.append(new)

                curr=curr.ischild[ord(seq[i])-ord("A")]
        
        

        return root


    def dfs(self,prefix,source,currdb,length):
        # if("#A"==prefix+source.val):
            # print("*****",source.count)
        if(len(prefix+source.val)>4+length):
            currdb.append((prefix,source))
            return True
        
        # discarded.append((prefix+source.val)

        # if(prefix+source.val not in self.frequent):
        self.frequent.update({prefix+source.val:source.count})
 


        # print(len(source.chu))
        for i in range(len(source.children)):
            if(source.children[i].count>=self.min_sup):
                self.dfs(prefix+source.val,source.children[i],currdb,length)


    
    def mine_pdb(self,candidate,tree,pdbs):
        next_db=[]
        self.dfs("#",tree,next_db,2)
        curr=len(next_db)
        print(candidate,pdbs[candidate],next_db)
        while(len(next_db)>0):
            temp=[]
            for i in range(len(next_db)):

                self.dfs(next_db[i][0],next_db[i][1],temp,len(next_db[i][0]))
            next_db=temp
        
        # print(self.frequent)

        
    def startMine(self):
        """
            Pattern mining process will start from here
        """
        l1=self.getfreqs()
        self.frequent={}
       

        # print(self.symbol_freq[0])
        pdbs={i:[] for i in l1}
        for seq in data:
            for j in range(len(seq[1])-1):
                if(self.symbol_freq[ord(seq[1][j])-ord('A')]):
                    pdbs[seq[1][j]].append(seq[1][j+1:])
        

        for  candidate in l1:
            tree=self.FSpanTree(candidate,pdbs[candidate])
            discarded=[]
            next_db=[]
            self.mine_pdb(candidate,tree,pdbs)
        
        self.frequent["#A"]=self.symbol_freq[ord("A")-ord("A")]
        self.frequent["#G"]=self.symbol_freq[ord("G")-ord("A")]
        self.frequent["#C"]=self.symbol_freq[ord("C")-ord("A")]
        self.frequent["#T"]=self.symbol_freq[ord("T")-ord("A")]
        
       
        print(self.frequent)
        




"""Driver code"""

df=pd.read_csv("data/D1.csv")
data=df.values[:,1:]
c=0
for i in data:
    c+=len(i[1])
# print(0.4*c)
obj = FSpanMining(minsup=150,data=data)
obj.startMine()
interestingPatterns = obj.getPatterns()
# print(interestingPatterns)
obj.save("res.csv")




# print(interestingPatterns)
# print("Total number of interesting patterns:", len(interestingPatterns))
# obj.save("result.csv")
# memUSS = obj.getMemoryUSS()
# print("Total Memory in USS:", memUSS)
# memRSS = obj.getMemoryRSS()
# print("Total Memory in RSS", memRSS)
# run = obj.getRuntime()
# print("Total ExecutionTime in seconds:", run)



