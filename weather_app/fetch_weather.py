import requests
import sqlite3
from datetime import datetime

AREA_CODE = "130000"
URL = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{AREA_CODE}.json"

response = requests.get(URL)
data = response.json()

conn = sqlite3.connect("weather.db")
cur = conn.cursor()

# 今日〜数日の予報が入ってる
time_series = data[0]["timeSeries"][0]
dates = time_series["timeDefines"]
weathers = time_series["areas"][0]["weathers"]

for date, weather in zip(dates, weathers):
    cur.execute("""
    INSERT INTO weather_forecasts
    (area_code, forecast_date, weather, fetched_at)
    VALUES (?, ?, ?, ?)
    """, (
        AREA_CODE,
        date,
        weather,
        datetime.now().isoformat()
    ))

conn.commit()
conn.close()

print("Weather data saved to DB.")