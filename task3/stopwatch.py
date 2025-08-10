import tkinter as tk
import time
import sqlite3

# ===== Database Setup =====
def init_db():
    conn = sqlite3.connect("laps.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS laps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lap_time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_lap(lap_time):
    conn = sqlite3.connect("laps.db")
    c = conn.cursor()
    c.execute("INSERT INTO laps (lap_time) VALUES (?)", (lap_time,))
    conn.commit()
    conn.close()

# ===== Stopwatch Logic =====
class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        self.root.configure(bg="#1e1e1e")

        self.start_time = 0
        self.elapsed_time = 0
        self.running = False
        self.update_job = None

        # Timer Label
        self.timer_label = tk.Label(root, text="00:00:000", font=("Arial", 40), fg="white", bg="#1e1e1e")
        self.timer_label.pack(pady=20)

        # Buttons
        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack()

        tk.Button(btn_frame, text="Start", command=self.start, width=10, bg="#444", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Pause", command=self.pause, width=10, bg="#444", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Lap", command=self.lap, width=10, bg="#444", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset, width=10, bg="#444", fg="white").grid(row=0, column=3, padx=5)

        # Lap List
        self.lap_listbox = tk.Listbox(root, width=30, height=8, font=("Arial", 14))
        self.lap_listbox.pack(pady=10)

        # Load previous laps from DB
        self.load_laps()

    def update_display(self):
        now = int((time.time() - self.start_time) * 1000)
        total_time = self.elapsed_time + now
        minutes = total_time // 60000
        seconds = (total_time % 60000) // 1000
        milliseconds = total_time % 1000
        self.timer_label.config(text=f"{minutes:02}:{seconds:02}:{milliseconds:03}")
        if self.running:
            self.update_job = self.root.after(10, self.update_display)

    def start(self):
        if not self.running:
            self.start_time = time.time() - (self.elapsed_time / 1000)
            self.running = True
            self.update_display()

    def pause(self):
        if self.running:
            self.elapsed_time += int((time.time() - self.start_time) * 1000)
            self.running = False
            if self.update_job:
                self.root.after_cancel(self.update_job)

    def lap(self):
        lap_time = self.timer_label.cget("text")
        save_lap(lap_time)
        self.lap_listbox.insert(tk.END, lap_time)

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        if self.update_job:
            self.root.after_cancel(self.update_job)
        self.timer_label.config(text="00:00:000")

    def load_laps(self):
        conn = sqlite3.connect("laps.db")
        c = conn.cursor()
        c.execute("SELECT lap_time FROM laps")
        for row in c.fetchall():
            self.lap_listbox.insert(tk.END, row[0])
        conn.close()

# ===== Run App =====
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
