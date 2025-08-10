import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  task TEXT NOT NULL,
                  completed INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    conn.close()
    return rows

def add_task(task):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, completed) VALUES (?, 0)", (task,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def edit_task(task_id, new_task):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET task=? WHERE id=?", (new_task, task_id))
    conn.commit()
    conn.close()

def toggle_task(task_id, completed):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed=? WHERE id=?", (completed, task_id))
    conn.commit()
    conn.close()

def refresh_list():
    for widget in task_frame.winfo_children():
        widget.destroy()

    tasks = get_tasks()
    for task in tasks:
        task_id, task_text, completed = task

        task_row = tk.Frame(task_frame, bg="#1e1e1e")
        task_row.pack(fill="x", padx=5, pady=2)

        var = tk.IntVar(value=completed)
        chk = tk.Checkbutton(task_row, text=task_text,
                             variable=var,
                             command=lambda t_id=task_id, v=var: toggle_and_refresh(t_id, v.get()),
                             font=("Arial", 12),
                             anchor="w", bg="#1e1e1e", fg="white", selectcolor="#1e1e1e")
        chk.pack(side="left", fill="x", expand=True)

        # Strike-through if completed
        if completed:
            chk.config(fg="gray", font=("Arial", 12, "overstrike"))

        # Edit Button
        edit_btn = tk.Button(task_row, text="✏", command=lambda t_id=task_id, t_text=task_text: edit_task_ui(t_id, t_text),
                             bg="#ffa500", fg="white", relief="flat", width=3)
        edit_btn.pack(side="right", padx=2)

        # Delete Button
        del_btn = tk.Button(task_row, text="🗑", command=lambda t_id=task_id: delete_task_ui(t_id),
                            bg="#f44336", fg="white", relief="flat", width=3)
        del_btn.pack(side="right", padx=2)

def toggle_and_refresh(task_id, completed_value):
    toggle_task(task_id, completed_value)
    refresh_list()

def add_task_ui():
    task = task_entry.get().strip()
    if not task:
        messagebox.showwarning("Input Error", "Please enter a task")
        return
    add_task(task)
    task_entry.delete(0, tk.END)
    refresh_list()

def delete_task_ui(task_id):
    delete_task(task_id)
    refresh_list()

def edit_task_ui(task_id, old_task):
    new_task = simpledialog.askstring("Edit Task", "Enter new task:", initialvalue=old_task)
    if new_task and new_task.strip():
        edit_task(task_id, new_task.strip())
        refresh_list()

root = tk.Tk()
root.title("📝 To-Do List with Checkboxes")
root.geometry("400x500")
root.configure(bg="#1e1e1e")

# Entry and Add Button
task_entry = tk.Entry(root, font=("Arial", 12), width=25)
task_entry.pack(pady=10)

add_button = tk.Button(root, text="Add Task", command=add_task_ui, bg="#4cafef", fg="white", relief="flat")
add_button.pack(pady=5)

# Scrollable Task List
canvas = tk.Canvas(root, bg="#1e1e1e", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
task_frame = tk.Frame(canvas, bg="#1e1e1e")

task_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=task_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

init_db()
refresh_list()

root.mainloop()

