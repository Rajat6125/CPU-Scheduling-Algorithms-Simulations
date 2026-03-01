import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from PIL import Image, ImageTk
import time

# ==========================================
# ROUNDED BUTTON CLASS
# ==========================================
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text,
                 width=280, height=100,
                 radius=25,
                 bg_color="#5A67D8",
                 hover_color="#434190",
                 click_color="#2B2F77",
                 text_color="white",
                 command=None):

        super().__init__(parent,
                         width=width,
                         height=height,
                         bg=parent["bg"],
                         highlightthickness=0)

        self.command = command
        self.default_bg = bg_color
        self.hover_bg = hover_color
        self.click_bg = click_color

        self.rect = self.create_rounded_rect(
            3, 3, width-3, height-3, radius,
            fill=self.default_bg
        )

        self.label = self.create_text(
            width/2,
            height/2,
            text=text,
            fill=text_color,
            font=("Segoe UI", 13, "bold"),
            width=width - 30,
            justify="center"
        )

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_hover(self, event):
        self.itemconfig(self.rect, fill=self.hover_bg)

    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.default_bg)

    def on_click(self, event):
        self.itemconfig(self.rect, fill=self.click_bg)

    def on_release(self, event):
        self.itemconfig(self.rect, fill=self.hover_bg)
        if self.command:
            self.command()


# ==========================================
# CORRECTED SCHEDULING ALGORITHMS
# ==========================================
def fcfs_cpu_scheduling(processes):
    original_order = list(processes.keys())
    # Sort by arrival time
    queue = sorted(processes.items(), key=lambda x: x[1][0])
    
    time = 0
    avg_tat = 0
    avg_wt = 0
    timeline = []
    result = {}
    
    for pname, pdata in queue:
        if pdata[0] > time:
            time = pdata[0]
        start = time
        time += pdata[1]
        end = time
        timeline.append((pname, start, end))
        
        ct = end
        tat = ct - pdata[0]
        wt = tat - pdata[1]
        
        result[pname] = [pdata[0], pdata[1], ct, tat, wt]
        avg_tat += tat
        avg_wt += wt
    
    # Reorder to original order
    ordered_result = {p: result[p] for p in original_order}
    res = pd.DataFrame.from_dict(ordered_result, orient='index',
                                columns=['AT', 'BT', 'CT', 'TAT', 'WT'])
    
    return timeline, res, avg_tat/len(processes), avg_wt/len(processes)

def sjf_cpu_scheduling(processes):
    original_order = list(processes.keys())
    # Sort by arrival time first
    queue = sorted(processes.items(), key=lambda x: x[1][0])
    
    time = 0
    avg_tat = 0
    avg_wt = 0
    completed = []
    remaining = queue.copy()
    timeline = []
    result = {}
    
    while remaining:
        # Get ready processes
        ready = [p for p in remaining if p[1][0] <= time]
        
        if not ready:
            time = min(p[1][0] for p in remaining)
            continue
        
        # Select shortest job
        shortest = min(ready, key=lambda x: x[1][1])
        remaining.remove(shortest)
        
        start = time
        time += shortest[1][1]
        end = time
        timeline.append((shortest[0], start, end))
        
        ct = end
        tat = ct - shortest[1][0]
        wt = tat - shortest[1][1]
        
        result[shortest[0]] = [shortest[1][0], shortest[1][1], ct, tat, wt]
        avg_tat += tat
        avg_wt += wt
    
    # Reorder to original order
    ordered_result = {p: result[p] for p in original_order}
    res = pd.DataFrame.from_dict(ordered_result, orient='index',
                                columns=['AT', 'BT', 'CT', 'TAT', 'WT'])
    
    return timeline, res, avg_tat/len(processes), avg_wt/len(processes)

def priority_scheduling_np(processes):
    original_order = list(processes.keys())
    # Sort by arrival time
    queue = sorted(processes.items(), key=lambda x: x[1][0])
    
    time = 0
    avg_tat = 0
    avg_wt = 0
    completed = []
    remaining = queue.copy()
    timeline = []
    result = {}
    
    while remaining:
        # Get ready processes
        ready = [p for p in remaining if p[1][0] <= time]
        
        if not ready:
            time = min(p[1][0] for p in remaining)
            continue
        
        # Select highest priority (lowest number)
        highest = min(ready, key=lambda x: x[1][2])
        remaining.remove(highest)
        
        start = time
        time += highest[1][1]
        end = time
        timeline.append((highest[0], start, end))
        
        ct = end
        tat = ct - highest[1][0]
        wt = tat - highest[1][1]
        
        result[highest[0]] = [highest[1][0], highest[1][1], highest[1][2], ct, tat, wt]
        avg_tat += tat
        avg_wt += wt
    
    # Reorder to original order
    ordered_result = {p: result[p] for p in original_order}
    res = pd.DataFrame.from_dict(ordered_result, orient='index',
                                columns=['AT', 'BT', 'P', 'CT', 'TAT', 'WT'])
    
    return timeline, res, avg_tat/len(processes), avg_wt/len(processes)

def shortest_job_first_p(processes):
    original_order = list(processes.keys())
    
    # Store original burst times
    burst_remaining = {p: processes[p][1] for p in processes}
    arrival_time = {p: processes[p][0] for p in processes}
    completion_time = {}
    
    time = 0
    completed = 0
    n = len(processes)
    timeline = []
    last_process = None
    start_time = None
    
    while completed < n:
        # Get available processes
        available = [p for p in processes if arrival_time[p] <= time and burst_remaining[p] > 0]
        
        if not available:
            time += 1
            continue
        
        # Select process with shortest remaining time
        current = min(available, key=lambda x: burst_remaining[x])
        
        if current != last_process:
            if last_process is not None:
                timeline.append((last_process, start_time, time))
            last_process = current
            start_time = time
        
        # Execute for 1 time unit
        burst_remaining[current] -= 1
        time += 1
        
        # Check if process completed
        if burst_remaining[current] == 0:
            completion_time[current] = time
            timeline.append((current, start_time, time))
            completed += 1
            last_process = None
    
    # Calculate results
    avg_tat = 0
    avg_wt = 0
    result = {}
    
    for p in processes:
        at = processes[p][0]
        bt = processes[p][1]
        ct = completion_time[p]
        tat = ct - at
        wt = tat - bt
        
        avg_tat += tat
        avg_wt += wt
        result[p] = [at, bt, ct, tat, wt]
    
    # Reorder to original order
    ordered_result = {p: result[p] for p in original_order}
    res = pd.DataFrame.from_dict(ordered_result, orient='index',
                                columns=['AT', 'BT', 'CT', 'TAT', 'WT'])
    
    return timeline, res, avg_tat/n, avg_wt/n

def round_robin(processes, time_quantum):
    original_order = list(processes.keys())
    
    # Store original burst times
    burst_remaining = {p: processes[p][1] for p in processes}
    arrival_time = {p: processes[p][0] for p in processes}
    completion_time = {}
    
    time = 0
    completed = 0
    n = len(processes)
    timeline = []
    ready_queue = []
    process_list = list(processes.keys())
    
    # Sort by arrival time
    process_list.sort(key=lambda x: arrival_time[x])
    
    current_index = 0
    last_process = None
    start_time = None
    
    while completed < n:
        # Add newly arrived processes to ready queue
        while current_index < n and arrival_time[process_list[current_index]] <= time:
            ready_queue.append(process_list[current_index])
            current_index += 1
        
        if not ready_queue:
            time += 1
            continue
        
        # Get next process from ready queue
        current = ready_queue.pop(0)
        
        if current != last_process:
            if last_process is not None:
                timeline.append((last_process, start_time, time))
            last_process = current
            start_time = time
        
        # Execute for time quantum or until completion
        exec_time = min(time_quantum, burst_remaining[current])
        time += exec_time
        burst_remaining[current] -= exec_time
        
        # Add newly arrived processes during execution
        while current_index < n and arrival_time[process_list[current_index]] <= time:
            ready_queue.append(process_list[current_index])
            current_index += 1
        
        # Check if process completed
        if burst_remaining[current] == 0:
            completion_time[current] = time
            timeline.append((current, start_time, time))
            completed += 1
            last_process = None
        else:
            # Re-add to ready queue
            ready_queue.append(current)
    
    # Calculate results
    avg_tat = 0
    avg_wt = 0
    result = {}
    
    for p in processes:
        at = processes[p][0]
        bt = processes[p][1]
        ct = completion_time[p]
        tat = ct - at
        wt = tat - bt
        
        avg_tat += tat
        avg_wt += wt
        result[p] = [at, bt, ct, tat, wt]
    
    # Reorder to original order
    ordered_result = {p: result[p] for p in original_order}
    res = pd.DataFrame.from_dict(ordered_result, orient='index',
                                columns=['AT', 'BT', 'CT', 'TAT', 'WT'])
    
    return timeline, res, avg_tat/n, avg_wt/n


# ==========================================
# MAIN WINDOW
# ==========================================
root = tk.Tk()
root.title("CPU Scheduling Algorithms")
root.geometry("1002x980")
root.configure(bg="#F3F4F6")
root.resizable(False, False)

# ==========================================
# PAGE SYSTEM
# ==========================================
container = tk.Frame(root, bg="#F3F4F6")
container.pack(fill="both", expand=True)

pages = {}

def show_page(name):
    pages[name].tkraise()

# ==========================================
# PAGE 1 (WITH LOGO)
# ==========================================
page1 = tk.Frame(container, bg="#F3F4F6")
page1.grid(row=0, column=0, sticky="nsew")
pages["main"] = page1

title_label = tk.Label(
    page1,
    text="CPU Scheduling Algorithms",
    font=("Impact", 36),
    bg="#F3F4F6",
    fg="#1F2937"
)
title_label.pack(pady=(40, 15))

# Logo
try:
    logo_image = Image.open("OS.png")
    logo_image = logo_image.resize((120, 80), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(page1, image=logo_photo, bg="#F3F4F6")
    logo_label.image = logo_photo
    logo_label.pack(pady=(0, 50))
except:
    # Fallback if image not found
    logo_canvas = tk.Canvas(page1, width=120, height=80,
                            bg="#F3F4F6", highlightthickness=0)
    logo_canvas.pack(pady=(0, 50))
    logo_canvas.create_oval(10, 10, 110, 70, fill="#3B82F6", outline="")
    logo_canvas.create_text(60, 40, text="CPU",
                            fill="white",
                            font=("Segoe UI", 16, "bold"))

main_frame = tk.Frame(page1, bg="#F3F4F6")
main_frame.pack(expand=True)

def open_algorithm(algo_name):
    build_second_page(algo_name)
    show_page("second")

# Non-Preemptive
np_label = tk.Label(main_frame,
    text="Non-Preemptive Algorithm",
    font=("Segoe UI", 20, "bold"),
    fg="#374151",
    bg="#F3F4F6")
np_label.pack(pady=(0, 50))

np_frame = tk.Frame(main_frame, bg="#F3F4F6")
np_frame.pack(pady=(0, 150))

RoundedButton(np_frame, "First Come First Serve",
              bg_color="#EF4444",
              hover_color="#DC2626",
              click_color="#B91C1C",
              command=lambda: open_algorithm("First Come First Serve")
              ).grid(row=0, column=0, padx=20)

RoundedButton(np_frame, "Shortest Job First",
              bg_color="#8B5CF6",
              hover_color="#7C3AED",
              click_color="#6D28D9",
              command=lambda: open_algorithm("Shortest Job First")
              ).grid(row=0, column=1, padx=20)

RoundedButton(np_frame, "Priority Scheduling",
              bg_color="#10B981",
              hover_color="#059669",
              click_color="#047857",
              command=lambda: open_algorithm("Priority Scheduling")
              ).grid(row=0, column=2, padx=20)

# Preemptive
p_label = tk.Label(main_frame,
    text="Pre-emptive Algorithm",
    font=("Segoe UI", 20, "bold"),
    fg="#374151",
    bg="#F3F4F6")
p_label.pack(pady=(0, 50))

p_frame = tk.Frame(main_frame, bg="#F3F4F6")
p_frame.pack()

RoundedButton(p_frame, "Shortest Remaining Time First",
              bg_color="#3B82F6",
              hover_color="#2563EB",
              click_color="#1D4ED8",
              command=lambda: open_algorithm("Shortest Remaining Time First")
              ).grid(row=0, column=0, padx=40)

RoundedButton(p_frame, "Round Robin",
              bg_color="#F59E0B",
              hover_color="#D97706",
              click_color="#B45309",
              command=lambda: open_algorithm("Round Robin")
              ).grid(row=0, column=1, padx=40)

# ==========================================
# PAGE 2
# ==========================================
page2 = tk.Frame(container, bg="#EEF2F7")
page2.grid(row=0, column=0, sticky="nsew")
pages["second"] = page2

# ==========================================
# PAGE 3 (RESULTS PAGE)
# ==========================================
page3 = tk.Frame(container, bg="#EEF2F7")
page3.grid(row=0, column=0, sticky="nsew")
pages["results"] = page3

# Global variables
current_algo = None
process_entries = []
quantum_entry = None
results_data = None

def build_second_page(selected_algo):
    global current_algo, process_entries, quantum_entry
    current_algo = selected_algo
    
    for widget in page2.winfo_children():
        widget.destroy()

    tk.Label(page2,
             text="CPU Scheduling Algorithms",
             font=("Impact", 34),
             bg="#EEF2F7",
             fg="#1E293B").pack(pady=(40, 20))

    tk.Label(page2,
             text=selected_algo,
             font=("Segoe UI", 16, "bold"),
             bg="#38BDF8",
             fg="white",
             padx=20,
             pady=8).pack(pady=10)

    input_frame = tk.Frame(page2, bg="#EEF2F7")
    input_frame.pack(pady=20)

    tk.Label(input_frame,
             text="Number of Processes:",
             font=("Segoe UI", 15),
             bg="#EEF2F7").grid(row=0, column=0, padx=10)

    process_entry = tk.Entry(input_frame, font=("Segoe UI", 14))
    process_entry.grid(row=0, column=1, padx=10)

    tk.Button(input_frame,
              text="Generate",
              command=lambda: generate_table(process_entry.get()),
              bg="#2563EB",
              fg="white",
              activebackground="#1D4ED8",
              font=("Segoe UI", 11, "bold"),
              relief="flat",
              bd=0,
              padx=12,
              pady=6,
              cursor="hand2"
              ).grid(row=0, column=2, padx=15)

    table_container = tk.Frame(page2, bg="#EEF2F7")
    table_container.pack(expand=True)

    global table_frame
    table_frame = tk.Frame(table_container, bg="#EEF2F7")
    table_frame.pack()

    # Round Robin Quantum
    if selected_algo == "Round Robin":
        tk.Label(input_frame,
                 text="Time Quantum:",
                 font=("Segoe UI", 15),
                 bg="#EEF2F7").grid(row=1, column=0, pady=10)

        quantum_entry = tk.Entry(input_frame, font=("Segoe UI", 14))
        quantum_entry.grid(row=1, column=1, pady=10)

    bottom = tk.Frame(page2, bg="#EEF2F7")
    bottom.pack(side="bottom", pady=25)

    tk.Button(bottom,
              text="◀ Back",
              bg="#EF4444",
              fg="white",
              activebackground="#DC2626",
              font=("Segoe UI", 13, "bold"),
              width=16,
              height=1,
              relief="flat",
              bd=0,
              cursor="hand2",
              command=lambda: show_page("main")
              ).grid(row=0, column=0, padx=30)

    tk.Button(bottom,
              text="Run ▶",
              bg="#10B981",
              fg="white",
              activebackground="#059669",
              font=("Segoe UI", 13, "bold"),
              width=16,
              height=1,
              relief="flat",
              bd=0,
              cursor="hand2",
              command=run_algorithm
              ).grid(row=0, column=1, padx=30)

def generate_table(n_str):
    global process_entries
    
    try:
        n = int(n_str)
    except:
        messagebox.showerror("Error", "Please enter a valid number")
        return
    
    for widget in table_frame.winfo_children():
        widget.destroy()
    
    process_entries = []
    
    show_priority = "Priority" in current_algo
    headers = ["Process", "Arrival Time", "Burst Time"]
    if show_priority:
        headers.append("Priority")
    
    for col, h in enumerate(headers):
        tk.Label(table_frame,
                 text=h,
                 font=("Segoe UI", 13, "bold"),
                 bg="#CBD5E1",
                 width=16).grid(row=0, column=col, padx=5, pady=5)
    
    for i in range(n):
        tk.Label(table_frame,
                 text=f"P{i+1}",
                 bg="#EEF2F7").grid(row=i+1, column=0, pady=5)
        
        row = []
        for col in range(1, len(headers)):
            e = tk.Entry(table_frame, width=15)
            e.grid(row=i+1, column=col, padx=5, pady=5)
            row.append(e)
        
        process_entries.append(row)

def run_algorithm():
    global results_data
    
    processes = {}
    try:
        for i, row_entries in enumerate(process_entries):
            pname = f"P{i+1}"
            at = int(row_entries[0].get())
            bt = int(row_entries[1].get())
            
            if "Priority" in current_algo:
                priority = int(row_entries[2].get())
                processes[pname] = [at, bt, priority]
            else:
                processes[pname] = [at, bt]
    except:
        messagebox.showerror("Error", "Please fill all fields with valid numbers")
        return
    
    quantum = None
    if current_algo == "Round Robin":
        try:
            quantum = int(quantum_entry.get())
        except:
            messagebox.showerror("Error", "Please enter a valid time quantum")
            return
    
    try:
        if current_algo == "First Come First Serve":
            results_data = fcfs_cpu_scheduling(processes)
        elif current_algo == "Shortest Job First":
            results_data = sjf_cpu_scheduling(processes)
        elif current_algo == "Priority Scheduling":
            results_data = priority_scheduling_np(processes)
        elif current_algo == "Shortest Remaining Time First":
            results_data = shortest_job_first_p(processes)
        elif current_algo == "Round Robin":
            results_data = round_robin(processes, quantum)
        
        build_results_page()
        show_page("results")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error running algorithm: {str(e)}")

def build_results_page():
    for widget in page3.winfo_children():
        widget.destroy()
    
    timeline, df, avg_tat, avg_wt = results_data
    
    # Fixed Back Button at Top Right
    back_button = tk.Button(page3,
                           text="← Back",
                           bg="#EF4444",
                           fg="white",
                           activebackground="#DC2626",
                           font=("Segoe UI", 11, "bold"),
                           width=8,
                           height=1,
                           relief="flat",
                           bd=0,
                           cursor="hand2",
                           command=lambda: show_page("second"))
    back_button.place(relx=0.95, rely=0.02, anchor="ne")
    
    # Main container
    main_container = tk.Frame(page3, bg="#EEF2F7")
    main_container.pack(expand=True, fill="both", padx=20, pady=(50, 15))
    
    # Title Section
    title_frame = tk.Frame(main_container, bg="#EEF2F7")
    title_frame.pack(fill="x", pady=(0, 10))
    
    title_label = tk.Label(title_frame,
                          text="CPU Scheduling Algorithms",
                          font=("Impact", 30),
                          bg="#EEF2F7",
                          fg="#1E293B")
    title_label.pack()
    
    algo_label = tk.Label(title_frame,
                         text=current_algo,
                         font=("Segoe UI", 14, "bold"),
                         bg="#38BDF8",
                         fg="white",
                         padx=20,
                         pady=5)
    algo_label.pack(pady=5)
    
    # Gantt Chart Section
    gantt_frame = tk.Frame(main_container, bg="#FFFFFF", relief="solid", borderwidth=1)
    gantt_frame.pack(fill="x", pady=10)
    
    gantt_header = tk.Frame(gantt_frame, bg="#F8FAFC")
    gantt_header.pack(fill="x", padx=1, pady=1)
    
    tk.Label(gantt_header,
            text="Gantt Chart",
            font=("Segoe UI", 14, "bold"),
            bg="#F8FAFC",
            fg="#334155").pack(pady=8)
    
    # Canvas for Gantt
    canvas_container = tk.Frame(gantt_frame, bg="#FFFFFF", height=120)
    canvas_container.pack(fill="x", padx=15, pady=10)
    canvas_container.pack_propagate(False)
    
    canvas = tk.Canvas(canvas_container, bg="#FFFFFF", highlightthickness=0, height=100)
    canvas.pack()
    
    # Calculate dimensions
    max_time = max(end for _, _, end in timeline)
    gantt_width = 800
    x_scale = gantt_width / max_time if max_time > 0 else 1
    
    colors = ['#FF6B6B', '#4ECDC4', '#FFD93D', '#6C5CE7', '#A8E6CF', '#FF8B94', '#A3C4F3']
    
    # Store segments
    segments = []
    current_x = 50
    for i, (process, start, end) in enumerate(timeline):
        width = (end - start) * x_scale
        segments.append({
            'process': process,
            'x': current_x,
            'width': width,
            'color': colors[i % len(colors)],
            'start_time': start,
            'end_time': end
        })
        current_x += width
    
    total_width = current_x
    canvas.configure(width=total_width + 50)
    
    # Draw time axis
    canvas.create_line(45, 70, total_width + 5, 70, width=2, fill="#94A3B8")
    
    # Time markers
    current_x = 50
    for seg in segments:
        canvas.create_text(seg['x'], 85, text=str(seg['start_time']), 
                          font=("Segoe UI", 9), fill="#475569")
        current_x = seg['x'] + seg['width']
    canvas.create_text(current_x, 85, text=str(max_time), 
                      font=("Segoe UI", 9), fill="#475569")
    
    # Process Table Section with Decent Colors
    table_frame = tk.Frame(main_container, bg="#FFFFFF", relief="solid", borderwidth=1)
    table_frame.pack(fill="both", expand=True, pady=10)
    
    table_header = tk.Frame(table_frame, bg="#F8FAFC")
    table_header.pack(fill="x", padx=1, pady=1)
    
    tk.Label(table_header,
            text="Process Table",
            font=("Segoe UI", 14, "bold"),
            bg="#F8FAFC",
            fg="#334155").pack(pady=8)
    
    # Table container
    table_container = tk.Frame(table_frame, bg="#FFFFFF")
    table_container.pack(fill="both", expand=True, padx=15, pady=10)
    
    # Averages Section - Left Aligned
    avg_frame = tk.Frame(main_container, bg="#FFFFFF", relief="solid", borderwidth=1)
    avg_frame.pack(fill="x", pady=10)
    
    avg_header = tk.Frame(avg_frame, bg="#F8FAFC")
    avg_header.pack(fill="x", padx=1, pady=1)
    
    tk.Label(avg_header,
            text="Calculated Values",
            font=("Segoe UI", 14, "bold"),
            bg="#F8FAFC",
            fg="#334155").pack(pady=8)
    
    # Left-aligned container for averages
    avg_container = tk.Frame(avg_frame, bg="#F1F5F9")
    avg_container.pack(fill="x", padx=20, pady=15)
    
    # Animation state
    current_segment = 0
    animation_speed = 400
    
    def animate_segment():
        nonlocal current_segment
        
        if current_segment < len(segments):
            seg = segments[current_segment]
            
            # Draw segment
            canvas.create_rectangle(seg['x'], 20, seg['x'] + seg['width'], 60,
                                  fill=seg['color'], outline="black", width=2)
            canvas.create_text(seg['x'] + seg['width']/2, 40,
                             text=seg['process'],
                             font=("Segoe UI", 10, "bold"),
                             fill="white")
            
            current_segment += 1
            
            if current_segment < len(segments):
                canvas.after(animation_speed, animate_segment)
            else:
                canvas.after(500, show_table_and_averages)
    
    def show_table_and_averages():
        # Get columns
        if "P" in df.columns:
            columns = ['AT', 'BT', 'P', 'CT', 'TAT', 'WT']
        else:
            columns = ['AT', 'BT', 'CT', 'TAT', 'WT']
        
        col_display = ["Process"] + columns
        
        # Create stylish table using ttk.Treeview
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure("Treeview",
                       background="#FFFFFF",
                       foreground="#1E293B",
                       rowheight=30,
                       fieldbackground="#FFFFFF",
                       font=("Segoe UI", 10))
        
        style.configure("Treeview.Heading",
                       background="#4F46E5",
                       foreground="white",
                       relief="flat",
                       font=("Segoe UI", 11, "bold"))
        
        style.map("Treeview.Heading",
                 background=[('active', '#6366F1')])
        
        style.map("Treeview",
                 background=[('selected', '#E0E7FF')],
                 foreground=[('selected', '#1E293B')])
        
        # Create treeview with scrollbar
        tree_frame = tk.Frame(table_container)
        tree_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(tree_frame, columns=col_display, show='headings',
                           yscrollcommand=scrollbar.set, height=6)
        scrollbar.config(command=tree.yview)
        
        # Configure columns with alternating header colors
        for i, col in enumerate(col_display):
            tree.heading(col, text=col)
            tree.column(col, width=90, anchor='center')
        
        # Add data with alternating row colors
        for index, process in enumerate(df.index):
            row_data = [df.loc[process, col] for col in columns]
            
            # Alternate row background
            if index % 2 == 0:
                tag = 'evenrow'
            else:
                tag = 'oddrow'
            
            tree.insert('', 'end', values=[process] + row_data, tags=(tag,))
        
        # Configure row tags
        tree.tag_configure('evenrow', background='#F8FAFC')
        tree.tag_configure('oddrow', background='#FFFFFF')
        
        tree.pack(side="left", fill="both", expand=True)
        
        # Left-aligned averages with typewriter effect
        avg_inner = tk.Frame(avg_container, bg="#F1F5F9")
        avg_inner.pack(anchor='w', padx=10)
        
        tat_text = f"Average Turnaround Time: {avg_tat:.2f}"
        wt_text = f"Average Waiting Time: {avg_wt:.2f}"
        
        tat_label = tk.Label(avg_inner,
                            text="",
                            font=("Segoe UI", 12, "bold"),
                            bg="#F1F5F9",
                            fg="#0F172A")
        tat_label.pack(anchor='w', pady=3)
        
        wt_label = tk.Label(avg_inner,
                           text="",
                           font=("Segoe UI", 12, "bold"),
                           bg="#F1F5F9",
                           fg="#0F172A")
        wt_label.pack(anchor='w', pady=3)
        
        def typewriter_tat(index=0):
            if index <= len(tat_text):
                tat_label.config(text=tat_text[:index])
                avg_inner.after(30, lambda: typewriter_tat(index + 1))
            else:
                typewriter_wt()
        
        def typewriter_wt(index=0):
            if index <= len(wt_text):
                wt_label.config(text=wt_text[:index])
                avg_inner.after(30, lambda: typewriter_wt(index + 1))
        
        typewriter_tat()
    
    # Start animation
    animate_segment()


# ==========================================
# START APP
# ==========================================
show_page("main")
root.mainloop()