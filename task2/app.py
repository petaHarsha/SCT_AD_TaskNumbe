from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create DB if not exists
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task'].strip()
    if task:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    new_task = request.form['new_task'].strip()
    if new_task:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET task=? WHERE id=?", (new_task, id))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
