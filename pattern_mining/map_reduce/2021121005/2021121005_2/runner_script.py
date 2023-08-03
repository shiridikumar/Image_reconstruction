import sys
import os

f=open(sys.argv[2],"r+")
line=0
mat_flag=0
p=-1
st=[]
m,n=0,0
for i in f.readlines():
    if(line==0 or p==0):
        args=list(map(int,i.split()))
        line=1
        if(p!=-1):
            mat_flag=1
            n=args[1]
        else:
            m=args[0]
        p=args[0]
    else:
        vals=list(map(int,i.split()))
        for j in range(len(vals)):
            st.append([str(args[0]),str(args[1]),str(line-1),str(j),str(vals[j]),str(mat_flag)])
            # st.append("{} {} {} {} {} {}\n".format(args[0],args[1],line-1,j,vals[j],mat_flag))
        p-=1
        line+=1

f.close()


temp=open("final_input.txt","w+")
for i in range(len(st)):
    st[i][0]=str(m);st[i][1]=str(n)
    temp.write(" ".join(st[i]))
    temp.write("\n")
temp.close()

# hadoop_jar=sys.argv[1]
hadoop_jar="/opt/hadoop-3.2.4/share/hadoop/tools/lib/hadoop-streaming-3.2.4.jar"
input_local=sys.argv[2]
file_name=os.path.basename(input_local)
input_hdfs=sys.argv[3]
output_hdfs=sys.argv[4]
mapreduce_dir=sys.argv[5]

os.system("hdfs dfs -rm -r "+os.path.join(sys.argv[3],"final_input.txt"))
copy_inp="hdfs dfs -copyFromLocal final_input.txt"+" "+input_hdfs
print(copy_inp)
os.system(copy_inp)
os.system("hdfs dfs -rm -r "+output_hdfs)

command="hadoop jar {} -file {} -mapper mapper.py -file {} -reducer reducer.py -input {} -output {}".format(hadoop_jar,os.path.join(mapreduce_dir,"mapper.py"),os.path.join(mapreduce_dir,"reducer.py"),os.path.join(sys.argv[3],"final_input.txt"),output_hdfs)
print(command)
os.system(command)
