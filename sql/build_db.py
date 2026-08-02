import sqlite3

DB_PATH = "micron_financials.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("connected! Database file created (or opened).")

cur.execute("""
CREATE TABLE IF NOT EXISTS quarterly_financials (
    fiscal_quarter_end   TEXT PRIMARY KEY,
    fiscal_year          INTEGER NOT NULL,
    fiscal_quarter       INTEGER NOT NULL,
    revenue_musd         REAL NOT NULL,
    gross_profit_musd    REAL NOT NULL,
    gross_margin_pct     REAL NOT NULL,
    eps_diluted_usd      REAL NOT NULL,
    period_label         TEXT NOT NULL
);
""")

conn.commit()
print("Table created!")

cur.execute("""
INSERT OR IGNORE INTO quarterly_financials
(fiscal_quarter_end, fiscal_year, fiscal_quarter, revenue_musd,
 gross_profit_musd, gross_margin_pct, eps_diluted_usd, period_label)
VALUES ('2021-02-28', 2021, 2, 6236, 1649, 26.44, 0.53, 'pre_shortage');
""")

conn.commit()
print("First row inserted!")

rows = [
    ("2021-05-31", 2021, 3, 7422,  3126, 1.52),
    ("2021-08-31", 2021, 4, 8274,  3912, 2.38),
    ("2021-11-30", 2022, 1, 7687,  3565, 2.04),
    ("2022-02-28", 2022, 2, 7786,  3676, 2.00),
    ("2022-05-31", 2022, 3, 8642,  4035, 2.34),
    ("2022-08-31", 2022, 4, 6643,  2622, 1.37),
    ("2022-11-30", 2023, 1, 4085,   893, -0.18),
    ("2023-02-28", 2023, 2, 3693, -1206, -2.12),
    ("2023-05-31", 2023, 3, 3752,  -668, -1.73),
    ("2023-08-31", 2023, 4, 4010,  -435, -1.31),
    ("2023-11-30", 2024, 1, 4726,   -35, -1.12),
    ("2024-02-29", 2024, 2, 5824,  1079, 0.71),
    ("2024-05-31", 2024, 3, 6811,  1832, 0.30),
    ("2024-08-31", 2024, 4, 7750,  2737, 0.81),
    ("2024-11-30", 2025, 1, 8709,  3348, 1.67),
    ("2025-02-28", 2025, 2, 8053,  2963, 1.41),
    ("2025-05-31", 2025, 3, 9301,  3508, 1.68),
    ("2025-08-31", 2025, 4, 11315, 5054, 2.83),
    ("2025-11-30", 2026, 1, 13643, 7646, 4.60),
    ("2026-02-28", 2026, 2, 23860, 17755, 12.07),
    ("2026-05-31", 2026, 3, 41460, 35056, 24.67),
]

SHORTAGE_START = "2025-08-31"

for fq_end, fy, fq, rev, gp, eps in rows:
    gm_pct = round((gp / rev) * 100, 2)
    period_label = "shortage_era" if fq_end >= SHORTAGE_START else "pre_shortage"
    cur.execute(
        """INSERT OR IGNORE INTO quarterly_financials
           (fiscal_quarter_end, fiscal_year, fiscal_quarter, revenue_musd,
            gross_profit_musd, gross_margin_pct, eps_diluted_usd, period_label)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (fq_end, fy, fq, rev, gp, gm_pct, eps, period_label),
    )

conn.commit()
print("All remaining rows inserted!")

cur.execute("SELECT COUNT(*) FROM quarterly_financials")
count = cur.fetchone()[0]
print(f"Total rows in database: {count}")

conn.close()
