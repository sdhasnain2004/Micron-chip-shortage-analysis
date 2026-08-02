import sqlite3

DB_PATH = "micron_financials.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("connected! Database file created (or opened).")
