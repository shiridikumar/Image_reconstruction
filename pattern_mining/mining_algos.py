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

    def __init__(self,ming_IG,min_conf,data):
        self.min_IG=ming_IG
        self.min_conf=min_conf
        self.data=data

    def IG(self,pattern):
        information=0
        # print(self.unique)
        for i in pattern.seq:
            pr=self.symbol_freq[ord(i)-ord("A")]/self.total_length
            pr=-1*math.log(pr,self.unique)
           
            information+=pr
            # if("ATCG"==pattern.seq):
            #     print(pr,information,"_______")
       
    
        return information*pattern.count
    
    def confidence(self,pattern):
        starting=pattern.seq[0]
        return pattern.count/self.symbol_freq[ord(starting)-ord('A')]



    def build_spanning_tree(self):
        root=Node("#")
        window=4
        self.nodes={}
        for i in range(len(self.data)):
            for j in range(len(self.data[i][1])-window+1):
                curr=root
                sequence=self.data[i][1][j:j+window]
                for symbol in sequence:
                    if(curr.children[ord(symbol)-ord("A")]):
                        curr=curr.children[ord(symbol)-ord("A")]
                    else:
                        node=Node(symbol)
                        curr.children[ord(symbol)-ord("A")]=node
                        curr=curr.children[ord(symbol)-ord("A")]
                       
                curr.leaf=True
                curr.seq=sequence
                
                
                curr.count+=1
                if(self.data[i][0] in curr.freq):
                    curr.freq[self.data[i][0]].append(j+1)
                else:
                    curr.freq.update({self.data[i][0]:[j+1]})
                
                # if(curr.seq=="CGTT"):
                #     print(curr.freq)
                if(curr.seq not in self.nodes):
                    self.nodes.update({curr.seq:curr})
                else:
                    self.nodes[curr.seq]=curr
            
    

    
    def getfreqs(self):
        self.symbol_freq=[0 for i in range(26)]
        self.total_length=0
        for i in range(len(self.data)):
            seq=self.data[i][1]
            for i in seq:
                self.symbol_freq[ord(i)-ord("A")]+=1
            self.total_length+=len(seq)
        self.unique=0
        for i in range(len(self.symbol_freq)):
            if(self.symbol_freq[i]!=0):
                self.unique+=1
    

    def prune_candidates(self):
        new=[]
        # print()
        # print(self.symbol_freq,"***************************************")
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



            




    def startMine(self):
        """
            Pattern mining process will start from here
        """
        self.getfreqs()
        self.build_spanning_tree()
        self.candidates=[]
        self.all={}
        # print(self.nodes)
        for i in self.nodes:
            if(self.IG(self.nodes[i])>=self.min_IG):
                # print(self.nodes[i].seq,self.IG(self.nodes[i]),self.nodes[i].count)
                self.candidates.append(self.nodes[i])
                self.all.update({self.nodes[i].seq:self.nodes[i].count})
        candidate_length=5
        # print()
        self.prev=self.nodes
        self.vis={}

       
        while(len(self.candidates)>0):
            for i in range(len(self.candidates)):
                for j in range(i+1,len(self.candidates)):
                    node1=self.candidates[i]
                    node2=self.candidates[j]
                    if(node1.seq[1:]==node2.seq[:-1] or node2.seq[1:]==node1.seq[:-1]):
                        for id in node1.freq:
                            if(id in node2.freq):
                                lp=0
                                rp=0
                                while(lp<len(node1.freq[id]) and rp<len(node2.freq[id])):
                                   
                                    if(node1.freq[id][lp]==node2.freq[id][rp]+1 or node1.freq[id][lp]+1==node2.freq[id][rp]):
                                        new_pattern=node1.seq+node2.seq[-1]
                                        mi=node1.freq[id][lp]
                                        if(node1.freq[id][lp]==node2.freq[id][rp]+1):
                                            new_pattern=node2.seq+node1.seq[-1]
                                            mi=node2.freq[id][rp]
                                        
                                        # if(node1.seq=="ATCG" and node2.seq=="TCGT"):
                                        #     print(node1.freq[id][lp],node2.freq[id][rp],id,"****************",new_pattern)

                                            
                                        if(new_pattern in self.vis):
                                            self.vis[new_pattern].count+=1
                                            
                                        else:
                                            node=Node(new_pattern[0])
                                            node.seq=new_pattern
                                            self.vis.update({new_pattern:node})
                                            self.vis[new_pattern].count=1
                                        
                                        if(id not in node.freq):
                                            node.freq.update({id:[mi]})
                                        else:
                                            node.freq[id].append(mi)

                                    if(node1.freq[id][lp]<node2.freq[id][rp]):
                                        lp+=1
                                    else:
                                        rp+=1
            

            self.candidates=self.prune_candidates()
            for i in range(len(self.candidates)):
                self.all.update({self.candidates[i].seq:self.candidates[i].count})
            self.prev=self.vis
            self.vis={}
                                    

                                
                





            



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



