import sqlite3

conn = sqlite3.connect("micron_financials.db")
cur = conn.cursor()

# Pull the pre-shortage quarters
cur.execute("""
SELECT fiscal_quarter_end, revenue_musd
FROM quarterly_financials
WHERE period_label = 'pre_shortage'
ORDER BY fiscal_quarter_end
""")
pre_shortage_data = cur.fetchall()

for row in pre_shortage_data:
    print(row)

# Fit a simple trend line (linear regression) through the pre-shortage revenue
x_values = list(range(len(pre_shortage_data)))
y_values = [row[1] for row in pre_shortage_data]

n = len(x_values)
sum_x = sum(x_values)
sum_y = sum(y_values)
sum_xy = sum(x * y for x, y in zip(x_values, y_values))
sum_x2 = sum(x ** 2 for x in x_values)

slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
intercept = (sum_y - slope * sum_x) / n

print(f"Slope: {slope:.2f}  (avg revenue change per quarter)")
print(f"Intercept: {intercept:.2f}  (starting point of the trend line)")

# Pull the actual shortage-era data
cur.execute("""
SELECT fiscal_quarter_end, revenue_musd
FROM quarterly_financials
WHERE period_label = 'shortage_era'
ORDER BY fiscal_quarter_end
""")
shortage_data = cur.fetchall()

# Create a table to hold the forecast-vs-actual comparison
cur.execute("""
CREATE TABLE IF NOT EXISTS forecast_vs_actual (
    fiscal_quarter_end   TEXT PRIMARY KEY,
    naive_forecast_musd  REAL NOT NULL,
    actual_revenue_musd  REAL NOT NULL,
    gap_musd             REAL NOT NULL,
    gap_pct              REAL NOT NULL
);
""")
conn.commit()
print("forecast_vs_actual table ready!")

# Calculate the naive forecast for each shortage-era quarter, compare to actual, and save
print("\nDate       | Naive Forecast | Actual Revenue | Gap ($M) | Gap (%)")
print("-" * 70)

for i, (fq_end, actual_rev) in enumerate(shortage_data):
    quarter_number = len(pre_shortage_data) + i
    naive_forecast = intercept + slope * quarter_number
    gap_dollars = actual_rev - naive_forecast
    gap_pct = (gap_dollars / naive_forecast) * 100
    print(f"{fq_end} | {naive_forecast:>13,.0f} | {actual_rev:>14,.0f} | {gap_dollars:>8,.0f} | {gap_pct:>6.1f}%")

    cur.execute("""
        INSERT OR IGNORE INTO forecast_vs_actual
        (fiscal_quarter_end, naive_forecast_musd, actual_revenue_musd, gap_musd, gap_pct)
        VALUES (?, ?, ?, ?, ?)
    """, (fq_end, naive_forecast, actual_rev, gap_dollars, gap_pct))

conn.commit()
print("\nForecast results saved to database!")

conn.close()
