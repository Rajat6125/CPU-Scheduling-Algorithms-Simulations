# 🖥️ CPU Scheduling Algorithms Visualizer

An interactive desktop application built with **Python** and **Tkinter** that visualizes major CPU scheduling algorithms using animated Gantt charts and a clean professional UI.

---

## 🧠 What is CPU Scheduling?

CPU scheduling is an operating system mechanism that decides which process gets CPU time when multiple processes are ready for execution.

### Key Terms

- **Arrival Time (AT)** – Time when a process enters the ready queue  
- **Burst Time (BT)** – CPU time required by the process  
- **Completion Time (CT)** – Time when process finishes execution  
- **Turnaround Time (TAT)** = CT − AT  
- **Waiting Time (WT)** = TAT − BT  

### Performance Metrics

- **Average Turnaround Time**
- **Average Waiting Time**

---

## 🔄 Implemented Scheduling Algorithms

### Non-Preemptive

1. **First Come First Serve (FCFS)**  
   Processes execute in order of arrival.

2. **Shortest Job First (SJF)**  
   Process with smallest burst time executes first.

3. **Priority Scheduling (Non-Preemptive)**  
   Process with highest priority executes first.

---

### Preemptive

4. **Shortest Remaining Time First (SRTF)**  
   Preemptive version of SJF.

5. **Round Robin (RR)**  
   Each process gets fixed time quantum in circular order.

---

## ✨ Core Features

- 5 CPU Scheduling Algorithms
- Animated Gantt Chart Visualization
- Automatic TAT and WT Calculation
- Clean Multi-Page GUI
- Interactive Process Input
- Time Quantum & Priority Support
- Back Navigation Between Pages

---

## 🚀 Requirements

- Python 3.6+
- Tkinter
- Pandas
- Pillow

Install dependencies:

```bash
pip install pandas pillow
```

---

## 📖 How to Use

1. Run the application:

```bash
python CPU_Scheduling_Algorithms.py
```

2. Select a scheduling algorithm.

3. Enter:
   - Number of processes
   - Arrival Time
   - Burst Time
   - Priority (if required)
   - Time Quantum (for Round Robin)

4. Click **Run** to see:
   - Animated Gantt Chart
   - Process Table with CT, TAT, WT
   - Average Waiting & Turnaround Time

---

## 📊 Algorithm Time Complexity

| Algorithm | Time Complexity | Space Complexity |
|------------|----------------|-----------------|
| FCFS | O(n log n) | O(n) |
| SJF | O(n²) | O(n) |
| Priority | O(n²) | O(n) |
| SRTF | O(n²) | O(n) |
| Round Robin | O(n²) | O(n) |

---

## 🚧 Future Improvements

- Multi-core CPU scheduling visualization  
- Algorithm comparison mode  
- Export results to CSV/PDF  
- Dark mode support  
- Web-based version  

---

## 📌 Author

Developed as an Operating Systems simulation project.

Project Link: https://github.com/Rajat6125/CPU-Scheduling-Algorithms-Simulations
