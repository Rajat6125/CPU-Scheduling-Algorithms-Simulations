import tkinter as tk

# -----------------------------
# Rounded Button (No Overflow Version)
# -----------------------------
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
        self.width = width
        self.height = height

        self.rect = self.create_rounded_rect(
            3, 3, width-3, height-3, radius,
            fill=self.default_bg
        )

        # 🔥 TEXT WRAP FIX HERE
        self.label = self.create_text(
            width/2,
            height/2,
            text=text,
            fill=text_color,
            font=("Segoe UI", 13, "bold"),
            width=width - 30,      # <---- This forces wrapping
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

# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()
root.title("CPU Scheduling Algorithms")
root.geometry("1002x980")
root.resizable(False, False)
root.configure(bg="#F3F4F6")


# -----------------------------
# Title (Top)
# -----------------------------
title_label = tk.Label(
    root,
    text="CPU Scheduling Algorithms",
    font=("Impact", 36),
    bg="#F3F4F6",
    fg="#1F2937"
)
title_label.pack(pady=(40, 15))


# -----------------------------
# Simple Custom Logo (Drawn)
# -----------------------------
logo_canvas = tk.Canvas(root, width=120, height=80,
                        bg="#F3F4F6", highlightthickness=0)
logo_canvas.pack(pady=(0, 50))

# Draw modern circular CPU-like logo
logo_canvas.create_oval(10, 10, 110, 70, fill="#3B82F6", outline="")
logo_canvas.create_text(60, 40, text="CPU",
                        fill="white",
                        font=("Segoe UI", 16, "bold"))


# -----------------------------
# Main Container
# -----------------------------
main_frame = tk.Frame(root, bg="#F3F4F6")
main_frame.pack(expand=True)


# -----------------------------
# Non-Preemptive Section
# -----------------------------
np_label = tk.Label(
    main_frame,
    text="Non-Preemptive Algorithm",
    font=("Segoe UI", 20, "bold"),
    fg="#374151",
    bg="#F3F4F6"
)
np_label.pack(pady=(0, 50))

np_frame = tk.Frame(main_frame, bg="#F3F4F6")
np_frame.pack(pady=(0, 150))

# Perfect spacing calculation:
# 280*3 = 840
# padding 20*2 gaps = 40
# Total = 880 (fits inside 1002 safely)

RoundedButton(np_frame,
              "First Come First Serve",
              bg_color="#EF4444",
              hover_color="#DC2626",
              click_color="#B91C1C").grid(row=0, column=0, padx=20)

RoundedButton(np_frame,
              "Shortest Job First",
              bg_color="#8B5CF6",
              hover_color="#7C3AED",
              click_color="#6D28D9").grid(row=0, column=1, padx=20)

RoundedButton(np_frame,
              "Priority Scheduling",
              bg_color="#10B981",
              hover_color="#059669",
              click_color="#047857").grid(row=0, column=2, padx=20)


# -----------------------------
# Pre-emptive Section
# -----------------------------
p_label = tk.Label(
    main_frame,
    text="Pre-emptive Algorithm",
    font=("Segoe UI", 20, "bold"),
    fg="#374151",
    bg="#F3F4F6"
)
p_label.pack(pady=(0, 50))

p_frame = tk.Frame(main_frame, bg="#F3F4F6")
p_frame.pack()

RoundedButton(p_frame,
              "Shortest Remaining Time First",
              bg_color="#3B82F6",
              hover_color="#2563EB",
              click_color="#1D4ED8").grid(row=0, column=0, padx=40)

RoundedButton(p_frame,
              "Round Robin",
              bg_color="#F59E0B",
              hover_color="#D97706",
              click_color="#B45309").grid(row=0, column=1, padx=40)


# -----------------------------
# Run App
# -----------------------------
root.mainloop()