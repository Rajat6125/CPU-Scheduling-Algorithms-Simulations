import pandas as pd
def fcfs_cpu_scheduling(processes):
    queue=list(processes.items())
    for i in range(len(queue)):
        for j in range(0,len(queue)-i-1):
            if queue[j][1][0]>queue[j+1][1][0]:
                queue[j],queue[j+1]=queue[j+1],queue[j]
    queue=dict(queue)
    
    c=0
    avg_tat=0
    avg_wt=0
    for i in queue:
        if queue[i][0]>c:
            c=queue[i][0]
        c=c+queue[i][1]
    
        queue[i].append(c)                          # Completion Time Calculation                        
        queue[i].append(queue[i][2]-queue[i][0])    # Turn Around Time calculation       
        queue[i].append(queue[i][3]-queue[i][1])    # Waiting Time calculation
        avg_tat+=queue[i][3]
        avg_wt+=queue[i][4]
    
    res=pd.DataFrame.from_dict(queue,orient="index",columns=["AT","BT","CT","TAT","WT"])
    res.rename(columns={"index": "Process"}, inplace=True)
    print(res.to_string())
    print("\nProcess Execution: ",list(queue.keys()))
    print("Average Turn around Time:",avg_tat/len(queue))
    print("Average Waiting Time:",avg_wt/len(queue))
    
# processes={"P1":[3,5],"P2":[5,2],"P3":[6,4],"P4":[7,3],"P5":[9,1]}
processes={"P1":[0,10],"P2":[1,6],"P3":[3,2],"P4":[5,4]}
fcfs_cpu_scheduling(processes)
