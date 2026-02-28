import pandas as pd

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


processes = {
    "P1": [0,8,2],
    "P2": [1,3,4],
    "P3": [2,6,1],
    "P4": [3,4,3],
    "P5": [6,2,5]
}

priority_scheduling_np(processes)