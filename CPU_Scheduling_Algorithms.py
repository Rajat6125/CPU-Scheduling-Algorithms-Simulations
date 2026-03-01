import pandas as pd
import matplotlib.pyplot as plt


def fcfs_cpu_scheduling(processes):
    original_order=list(processes.keys())
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
    
    res = res.loc[original_order]
    res.rename(columns={"index": "Process"}, inplace=True)
    print(res.to_string())
    print("\nProcess Execution: ",list(queue.keys()))
    print("Average Turn around Time:",avg_tat/len(queue))
    print("Average Waiting Time:",avg_wt/len(queue))


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
    

def priority_scheduling_np(processes):
    original_order=list(processes.keys())
    queue=sorted(processes.items(),key=lambda x:x[1][0])
    
    time = 0 
    avg_tat = 0
    avg_wt = 0
    completed = []
    remaining = queue
    
    while remaining:
        ready=[]
        
        for i in remaining:
            if i[1][0]<=time:
                ready.append(i)
                
        if not ready:
            time=remaining[0][1][0]
            continue
        
        # Priority comparison
        high=ready[0]
        for j in ready:
            if j[1][2]<high[1][2]:
                high=j
        remaining.remove(high)
        
        time+=high[1][1]
        ct=time
        tat=ct-high[1][0]
        wt=tat-high[1][1]
        
        high[1].extend([ct,tat,wt])
        completed.append(high)
        avg_tat+=tat
        avg_wt+=wt
      
        
    completed = dict(completed)
    res=pd.DataFrame.from_dict(completed,orient='index',columns=['AT','BT','P','CT','TAT','WT'])
        
    res=res.loc[original_order]
        
    print(res.to_string())
    print("\nProcess Execution: ", list(completed.keys()))
    print("Average Turn Around Time:", avg_tat / len(completed))
    print("Average Waiting Time:", avg_wt / len(completed))


import pandas as pd

def shortest_job_first_p(processes):
    original_order = list(processes.keys())
    queue = sorted(processes.items(), key=lambda x: x[1][0])
    
    time = 0
    avg_tat = 0
    avg_wt = 0
    completed = []
    remaining = queue
    
    # To store original burst times
    burst_time = {p: processes[p][1] for p in processes}
    completion_time = {}
    
    while remaining:
        ready = []
        
        for i in remaining:
            if i[1][0] <= time:
                ready.append(i)
        
        
        if not ready:
            time = remaining[0][1][0]
            continue
        
        # Find shortest remaining burst
        short = ready[0]
        for j in ready:
            if j[1][1] < short[1][1]:
                short = j
        
        idx = remaining.index(short)
        pname, pdata = short
        
        
        new_burst = pdata[1] - 1
        time += 1
        
        if new_burst == 0:
            completion_time[pname] = time
            completed.append(pname)
            remaining.pop(idx)
        else:
            remaining[idx] = (pname, [pdata[0], new_burst])
    
    
    result = {}
    
    for p in processes:
        at = processes[p][0]
        bt = burst_time[p]
        ct = completion_time[p]
        tat = ct - at
        wt = tat - bt
        
        avg_tat += tat
        avg_wt += wt
        
        result[p] = [at, bt, ct, tat, wt]
    
    
    res = pd.DataFrame.from_dict(result, orient='index',
                                 columns=["AT","BT","CT","TAT","WT"])
    
    
    res = res.loc[original_order]
    
    print(res.to_string())
    print("\nProcess Completion Order:", completed)
    print("Average Turn around Time:", round(avg_tat/len(processes),2))
    print("Average Waiting Time:", round(avg_wt/len(processes),2))



def round_robin(processes, time_quantum):
    original_order = list(processes.keys())
    
    queue = sorted(processes.items(), key=lambda x: x[1][0])
    
    time = 0
    avg_tat = 0
    avg_wt = 0
    completed = []
    remaining = queue
    
    # Store original burst times
    burst_time = {p: processes[p][1] for p in processes}
    completion_time = {}
    
    while remaining:
        ready = []
        
        # Get all arrived processes
        for i in remaining:
            if i[1][0] <= time:
                ready.append(i)
        
        # If no process has arrived yet
        if not ready:
            time = remaining[0][1][0]
            continue
        
        # Pick first arrived process (FCFS order in RR)
        current = ready[0]
        idx = remaining.index(current)
        
        pname, pdata = current
        arrival, burst = pdata
        
        # Execute for time_quantum or remaining burst
        exec_time = min(time_quantum, burst)
        time += exec_time
        new_burst = burst - exec_time
        
        if new_burst == 0:
            completion_time[pname] = time
            completed.append(pname)
            remaining.pop(idx)
        else:
            # Update remaining burst
            remaining.pop(idx)
            remaining.append((pname, [arrival, new_burst]))
    
    
    result = {}
    
    for p in processes:
        at = processes[p][0]
        bt = burst_time[p]
        ct = completion_time[p]
        tat = ct - at
        wt = tat - bt
        
        avg_tat += tat
        avg_wt += wt
        
        result[p] = [at, bt, ct, tat, wt]
    
    
    res = pd.DataFrame.from_dict(result, orient='index',
                                 columns=["AT","BT","CT","TAT","WT"])
    
    res = res.loc[original_order]
    
    print(res.to_string())
    print("\nProcess Completion Order:", completed)
    print("Average Turn around Time:", round(avg_tat/len(processes),2))
    print("Average Waiting Time:", round(avg_wt/len(processes),2))



while True:
    print("Algorithms:\n")
    print("NON_PREMPTIVE ALGORITHMS\n 1.First Come First Serve\n 2.Shortest Job First\n 3.Priority Scheduling")
    print("PREMPTIVE ALGORITHMS\n 4.Shortest Job First\n 5.Round-Robin ")
    algo=int(input("Choose Algorithm: "))
    count=int(input("Number of Processes: "))
    processes={}
    quanta=0
    if algo in [1,2,4]:
        for i in range(count):
            pname=input("Process: ")
            pdata=[int(input("Arrival time: ")),int(input("Brust time: "))]
            processes[pname]=pdata
    
    elif algo==3:
        for i in range(count):
            pname=input("Process: ")
            pdata=[int(input("Arrival time: ")),int(input("Brust time: ")),int(input("Priority: "))]
            processes[pname]=pdata
    
    elif algo==4:
        quanta=int(input("Time Quantum: "))
        for i in range(count):
            pname=input("Process: ")
            pdata=[int(input("Arrival time: ")),int(input("Brust time: "))]
            processes[pname]=pdata
    
    if algo==1:
        fcfs_cpu_scheduling(processes)
    elif algo==2:
        sjf_cpu_scheduling(processes)
    elif algo==3:
        priority_scheduling_np(processes)
    elif algo==4:
        shortest_job_first_p(processes)
    elif algo==5:
        round_robin(processes,quanta)
    elif algo==6:
        break
    else:
        continue