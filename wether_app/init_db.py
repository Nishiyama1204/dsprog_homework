import sqlite3

conn = sqlite3.connect("weather.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS weather_forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_code TEXT NOT NULL,
    forecast_date TEXT NOT NULL,
    weather TEXT,
    temperature_min INTEGER,
    temperature_max INTEGER,
    fetched_at TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("DB initialized.")