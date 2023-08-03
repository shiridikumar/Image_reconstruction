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
        self.count=0
        self.seq=""




class SurpriseSeqMining:
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

    

    def prune_candidates(self):
        new=[]
        for i in self.vis:
            if(self.IG(self.vis[i])>=self.min_IG):
                # print(self.vis[i].seq,self.vis[i].count)
                
                new.append(self.vis[i])
        

        # print()
        return new
    

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns

        :rtype: dict
        """
        return self.all

    
    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe

        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        seqs=[]
        sup=[]
        for i in self.all:
            seqs.append(i)
            sup.append(self.all[i])


            
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
        writer = open(self._oFile, 'w+')
        seqs=[]
        sup=[]
        for i in self.all:
            seqs.append(i)
            sup.append(self.all[i])

        for i in range(len(seqs)):
            s1 = seqs[i] + ":" + str(sup[i])
            writer.write("%s \n" % s1)

    
    def get_projected_database(self,prefix):






            




    def startMine(self):
        """
            Pattern mining process will start from here
        """
        l1=self.getfreqs();
        for i in l1:
            pdb=self.get_project_database(i)

        

                                
                





            



"""Driver code"""

df=pd.read_csv("data/D1.csv")
data=df.values[:,1:]
c=0
for i in data:
    c+=len(i[1])
# print(0.4*c)
obj = SurpriseSeqMining(ming_IG=300,min_conf=0.3,data=data)
obj.startMine()
interestingPatterns = obj.getPatterns()
# print(interestingPatterns)
print("Total number of interesting patterns:", len(interestingPatterns))
obj.save("result.csv")
# memUSS = obj.getMemoryUSS()
# print("Total Memory in USS:", memUSS)
# memRSS = obj.getMemoryRSS()
# print("Total Memory in RSS", memRSS)
# run = obj.getRuntime()
# print("Total ExecutionTime in seconds:", run)



