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

processes={"P1":[0,10],
           "P2":[2,6],
           "P3":[4,4],
           "P4":[6,4],
           "P5":[7,1],
           "P6":[9,2]}
shortest_job_first_p(processes)
