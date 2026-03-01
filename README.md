## 🖥️ CPU Scheduling Algorithms Visual Simulator

A complete GUI-based CPU Scheduling Simulator built using Python (Tkinter + Pandas + ttk + PIL) that visually demonstrates how different CPU Scheduling Algorithms work using animated Gantt Charts and detailed result tables.

This project is specially designed for Operating System learners to understand scheduling concepts clearly through visualization and real-time calculation.

## 📌 Project Overview

CPU Scheduling is a fundamental concept in Operating Systems. It determines which process will use the CPU at any given time. Efficient scheduling improves:

CPU Utilization

Throughput

Turnaround Time

Waiting Time

Response Time

This simulator allows users to:

✔ Enter custom process data
✔ Run multiple scheduling algorithms
✔ Visualize execution using animated Gantt Chart
✔ View calculated metrics in a styled result table
✔ Compare average turnaround and waiting times

## 📖 Theory & Concepts
🔹 What is CPU Scheduling?

CPU Scheduling is the process of selecting one process from the ready queue to allocate the CPU. The scheduler decides the execution order based on a scheduling algorithm.

🔹 Important Terminologies
Term	Meaning
AT (Arrival Time)	Time at which process enters ready queue
BT (Burst Time)	CPU execution time required
CT (Completion Time)	Time at which process completes
TAT (Turnaround Time)	CT − AT
WT (Waiting Time)	TAT − BT
Priority	Process priority (lower number = higher priority)
Time Quantum	Fixed CPU time slice (Round Robin)
🧠 Implemented Algorithms
1️⃣ First Come First Serve (FCFS) – Non-Preemptive
📌 Concept

Processes are executed in the order they arrive.

Simple and easy to implement.

Can cause Convoy Effect (long job blocks short jobs).

⚙️ Working

Sort by Arrival Time.

Execute each process fully before moving to next.

2️⃣ Shortest Job First (SJF) – Non-Preemptive
📌 Concept

Process with smallest Burst Time is selected.

Reduces average waiting time.

Can cause starvation of longer jobs.

⚙️ Working

At each scheduling decision:

Select shortest job among arrived processes.

3️⃣ Priority Scheduling – Non-Preemptive
📌 Concept

Process with highest priority (lowest number) runs first.

Can lead to starvation of low-priority processes.

⚙️ Working

Among available processes, select one with minimum priority value.

4️⃣ Shortest Remaining Time First (SRTF) – Preemptive
📌 Concept

Preemptive version of SJF.

If a shorter job arrives, current job is preempted.

Minimizes average waiting time.

⚙️ Working

At every time unit:

Choose process with shortest remaining burst time.

Process switching handled dynamically.

5️⃣ Round Robin (RR) – Preemptive
📌 Concept

Each process gets fixed Time Quantum.

Fair scheduling.

Used in time-sharing systems.

⚙️ Working

Execute process for Time Quantum.

If not finished → move to end of ready queue.

Repeat until all complete.
