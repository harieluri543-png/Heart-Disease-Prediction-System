import sqlite3

conn = sqlite3.connect("heart.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    gender TEXT,
    prediction TEXT,
    confidence REAL,
    date TEXT,
    time TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")