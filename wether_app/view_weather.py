import sqlite3

AREA_CODE = "130000"

date_input = input("見たい日付を入力してください（例: 2026-01-13）: ")

conn = sqlite3.connect("weather.db")
cur = conn.cursor()

cur.execute("""
SELECT forecast_date, weather
FROM weather_forecasts
WHERE area_code = ?
AND forecast_date LIKE ?
ORDER BY forecast_date
""", (AREA_CODE, f"{date_input}%"))

rows = cur.fetchall()
conn.close()

print("=== 天気予報 ===")
if rows:
    for date, weather in rows:
        print(date, weather)
else:
    print("その日の予報はDBにありません。")