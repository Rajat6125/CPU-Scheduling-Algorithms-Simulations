import pandas as pd
def sjf_cpu_scheduling(processes):
    original_order=list(processes.keys())
    queue=list(processes.items())
    for i in range(len(queue)):
        for j in range(0,len(queue)-i-1):
            if queue[j][1][0]>queue[j+1][1][0]:
                queue[j],queue[j+1]=queue[j+1],queue[j]
                
    time=0
    avg_tat=0
    avg_wt=0
    completed=[]
    remaining=queue

    while remaining:
        ready=[]
        
        # If arrived
        for i in remaining:
            if i[1][0]<=time:
                ready.append(i)
        
        # If not arrived
        if not ready:
            time=remaining[0][1][0]
            continue
        
        # Sorting
        shortest=ready[0]
        for j in ready:
            if j[1][1]<shortest[1][1]:
                shortest=j
        remaining.remove(shortest)
        
        time+=shortest[1][1]
        ct=time
        tat=ct-shortest[1][0]
        wt=tat-shortest[1][1]
        
        shortest[1].extend([ct,tat,wt])
        completed.append(tuple(shortest))
        
    completed = dict(completed)

    for i in completed.items():
        avg_tat+=i[1][3]
        avg_wt+=i[1][4]

    res = pd.DataFrame.from_dict(completed, orient='index',
                                columns=["AT","BT","CT","TAT","WT"])

    # Reorder according to original input order
    res = res.loc[original_order]

    res.rename(columns={"index": "Process"}, inplace=True)
    print(res.to_string())
    print("\nProcess Execution: ",list(completed.keys()))
    print("Average Turn around Time:",avg_tat/len(completed))
    print("Average Waiting Time:",avg_wt/len(completed))
    


# processes={"P1":[4,6],"P2":[2,3],"P3":[6,2],"P4":[5,4],"P5":[7,1]}

processes={"P1":[0,10],"P2":[1,6],"P3":[3,2],"P4":[5,4]}
sjf_cpu_scheduling(processes)