import sys
import os
# import pandas as pd

# input_path=sys.argv[1]
# df=pd.read_csv(input_path)
# vals=df.values
# f=open("mapreduce_input.txt","w+")
# for seq in vals:
#     for i in seq:
#         f.write(str(i)+",")
#     f.write("\n")
# f.close()


class MapReduce:

    def __init__(self,minsup,datapath,max_length_candidates=100):
        self.minsup=minsup
        self.datapath=datapath
        self.max_length_candidates=max_length_candidates
        pass

    def setPaths(self):
        self.hadoop_jar="/opt/hadoop-3.2.4/share/hadoop/tools/lib/hadoop-streaming-3.2.4.jar"
        self.mapper_path="/PositionMining/mapper1.py"
        self.reducer1_path="/PositionMining/reducer1.py"
        self.reducer2_path="/PositionMining/reducer2.py"
        self.reducer0_path="/PositionMining/reducer0.py"
        self.input_path="/input.txt"
        self.output_path="/output/out"

    def startMine(self):
        self.comm="hadoop jar /opt/hadoop-3.2.4/share/hadoop/tools/lib/hadoop-streaming-3.2.4.jar -file {} -mapper {} -file {} -reducer {}  -input {} -output {}"
        self.setPaths()
        try:
            os.system("rm -rf output")
        except:
            pass
        os.system("mkdir output")
        self.hadoop_commands=[]
        self.hadoop_commands.append("hdfs dfs -rm /input.txt")
        self.hadoop_commands.append("hdfs dfs -copyFromLocal mapreduce_input.txt /input.txt")
        # self.hadoop_commands.append()
        self.hadoop_commands.append(self.comm.format(self.mapper_path,"mapper1.py",self.reducer1_path,"reducer1.py",self.input_path,self.output_path+"1"))
        command1="cat {}".format(self.datapath)
        command1+=" | python3 mapper1.py  | sort | python3 reducer1.py " 
        prev_out="/output/out"

        for i in range(2,self.max_length_candidates+1):
            command=self.comm.format(self.mapper_path,"cat",self.reducer1_path,"reducer1.py",prev_out+str(i-1),prev_out+str(i))
            self.hadoop_commands.append(command)
            command1+=" |  sort | python3 reducer1.py "
        
            
        
        # print(command1)
        # os.system(command1)

        for i in self.hadoop_commands:
            os.system(i)
        
        

        self.reducer2_commands=[]
        final_out="/output/patterns_length_"
        for i in range(2,self.max_length_candidates+1):
            self.reducer2_commands.append(self.comm.format(self.mapper_path,"cat",self.reducer2_path,"reducer2.py",self.output_path+str(i),final_out+str(i)))
        

        for i in self.reducer2_commands:
            os.system(i)
        

            



alg=MapReduce(2,"mapreduce_input.txt",max_length_candidates=3)
alg.startMine()




            







# hadoop_jar="/opt/hadoop-3.2.4/share/hadoop/tools/lib/hadoop-streaming-3.2.4.jar"
# file_name=os.path.basename(input_local)




# os.system("hdfs dfs -rm -r "+os.path.join(sys.argv[3],"final_input.txt"))
# copy_inp="hdfs dfs -copyFromLocal final_input.txt"+" "+input_hdfs
# print(copy_inp)
# os.system(copy_inp)
# os.system("hdfs dfs -rm -r "+output_hdfs)

# command="hadoop jar {} -file {} -mapper mapper.py -file {} -reducer reducer.py -input {} -output {}".format(hadoop_jar,os.path.join(mapreduce_dir,"mapper.py"),os.path.join(mapreduce_dir,"reducer.py"),os.path.join(sys.argv[3],"final_input.txt"),output_hdfs)
# print(command)
# os.system(command)
