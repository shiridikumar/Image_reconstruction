import sys
import os
file="input.txt"

temp=open("final_input.txt","w+")
f=open(sys.argv[2],"r+")
for i in f.readlines():
    num=int(i)
for i in range(num):
    temp.write(str(i+1)+"\n")
f.close()
temp.close()

hadoop_jar=sys.argv[1]
# hadoop_jar="/opt/hadoop-3.2.4/share/hadoop/tools/lib/hadoop-streaming-3.2.4.jar"
input_local=sys.argv[2]
file_name=os.path.basename(input_local)
input_hdfs=sys.argv[3]
output_hdfs=sys.argv[4]
mapreduce_dir=sys.argv[5]

os.system("hdfs dfs -rm -r "+os.path.join(input_hdfs,"final_input.txt"))
copy_inp="hdfs dfs -copyFromLocal final_input.txt"+" "+input_hdfs
print(copy_inp)
os.system(copy_inp)
os.system("hdfs dfs -rm -r "+output_hdfs)

command="hadoop jar {} -file {} -mapper mapper.py -file {} -reducer reducer.py -input {} -output {}".format(hadoop_jar,os.path.join(mapreduce_dir,"mapper.py"),os.path.join(mapreduce_dir,"reducer.py"),os.path.join(input_hdfs,"final_input.txt"),output_hdfs)
print(command)
os.system(command)
