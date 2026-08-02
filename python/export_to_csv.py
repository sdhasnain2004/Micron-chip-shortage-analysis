import sqlite3
import csv

conn = sqlite3.connect("micron_financials.db")
cursor = conn.cursor()

for table in ["quarterly_financials", "forecast_vs_actual"]:
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    with open(f"{table}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print("Done exporting", table)

conn.close()
