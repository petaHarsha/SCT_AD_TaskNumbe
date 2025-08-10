import sqlite3

conn = sqlite3.connect("tasks.db")
c = conn.cursor()

# Add 'completed' column if it doesn't exist
try:
    c.execute("ALTER TABLE tasks ADD COLUMN completed INTEGER DEFAULT 0")
except sqlite3.OperationalError:
    print("Column already exists.")

conn.commit()
conn.close()
print("✅ Database updated with 'completed' column.")
