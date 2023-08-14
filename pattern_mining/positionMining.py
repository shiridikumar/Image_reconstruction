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
        self.children=[None for i in range(26)]
        self.leaf=leaf
        self.freq={}
        self.count=1
        self.seq=""




class PositionMining:
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
        """Initial scan of database where frequent length 1 candidates will be mined

        :param : none
        """
        self.symbol_freq={"A":set(),"G":set(),"C":set(),"T":set()}
        self.total_length=0
        curr_pos=0
        for i in range(len(self.data)):
            seq=self.data[i][1]
            for j in range(len(seq)):
                self.symbol_freq[seq[j]].add(curr_pos)
                curr_pos+=1
            curr_pos+=1
            self.total_length+=len(seq)

        temp={}
        for i in self.symbol_freq:
            if(len(self.symbol_freq[i])>=self.min_sup):
                temp.update({i:self.symbol_freq[i]})
        self.symbol_freq=temp

    
    

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns

        :rtype: dict
        """

        return self.frequentPatterns


    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe

        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        seqs=[]
        sup=[]
        for i in self.frequentPatterns:
            seqs.append(i)
            sup.append(self.frequentPatterns[i])


        dataFrame =pd.DataFrame()
        dataFrame["Patterns"]=seqs
        dataFrame["Support"]=sup
        return dataFrame


    def save(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: file
        """


        df=self.getPatternsAsDataFrame()
        df.to_csv(outFile)


    def getPattern_positions(self,pattern):
        length=len(pattern)
        positions=self.table[length][pattern]
        return positions


    def join(self,db,length):
        """ Generating l+1 frequent patterns using two l length frequent patterns

        :param db:current l length frequent patterns table consisiting of their positions
        :type db: HashTable

        :param length:current length of the frequent candidates generated
        :type length: positive integer

        """
        for seq1 in db:
            for seq2 in db:
                if(seq1!=seq2):
                    if(length==1):
                        word=seq1+seq2
                        # print(seq1,seq2,db[seq1],db[seq2])
                        minus_1={i-1 for i in db[seq2]}
                        positions=db[seq1].intersection(minus_1)
                        if(len(positions)>=self.min_sup):
                            self.table[length+1].update({word:positions})


                    else:
                        if(seq1[1:]== seq2[:-1]):
                            word=seq1+seq2[-1]
                            minus_1={i-1 for i in db[seq2]}
                            positions=db[seq1].intersection(minus_1)
                            if(len(positions)>=self.min_sup):
                                self.table[length+1].update({word:positions})
        

    def mineNext_candidates(self):
        """Minining frequent patterns along with their positions from length 1 frequent candidates

        :param : none
        """
        while self.current_candidate<5:
            curr=self.table[self.current_candidate]
            self.join(curr,self.current_candidate)
            self.current_candidate+=1


        
    def startMine(self):
        """
            Pattern mining process will start from here
        """
        self.table={i:{} for i in range(1,6)}
        self.getfreqs()
        temp=self.symbol_freq
        self.table.update({1:temp})
        self.current_candidate=1
        self.mineNext_candidates()
        self.frequentPatterns={}
        for length in self.table:
            temp=self.table[length]
            for pattern in temp:
                self.frequentPatterns.update({pattern:len(temp[pattern])})
    






"""Driver code"""

df=pd.read_csv("data/D2.csv")
data=df.values[:,1:]
c=0
for i in data:
    c+=len(i[1])

obj = PositionMining(minsup=2,data=data)
obj.startMine()
interestingPatterns = obj.getPatterns()
print(interestingPatterns)
print("Total number of interesting patterns:", len(interestingPatterns))
obj.save("result.csv")


print()
print()
# print("Positions where","TCTA is found \n\n",obj.getPattern_positions("TCTA"))


# memUSS = obj.getMemoryUSS()
# print("Total Memory in USS:", memUSS)
# memRSS = obj.getMemoryRSS()
# print("Total Memory in RSS", memRSS)
# run = obj.getRuntime()
# print("Total ExecutionTime in seconds:", run)



