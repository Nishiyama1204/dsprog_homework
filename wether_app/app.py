import flet as ft
import sqlite3
import subprocess

DB_NAME = "weather.db"
AREA_CODE = "130000"


def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.window_width = 600
    page.window_height = 500

    # --- UI部品 ---
    title = ft.Text("天気予報アプリ", size=24, weight="bold")

    date_input = ft.TextField(
        label="日付指定（例: 2026-01-13）",
        width=300
    )

    output = ft.Text(selectable=True)

    # --- 天気取得（API → DB） ---
    def fetch_weather(e):
        subprocess.run(["python", "fetch_weather.py"])
        output.value = "天気予報を取得しました"
        page.update()

    # --- 天気表示（DB → 画面） ---
    def show_weather(e):
        date = date_input.value

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        if date:
            cur.execute("""
            SELECT forecast_date, weather
            FROM weather_forecasts
            WHERE area_code = ?
            AND forecast_date LIKE ?
            ORDER BY forecast_date
            """, (AREA_CODE, f"{date}%"))
        else:
            cur.execute("""
            SELECT forecast_date, weather
            FROM weather_forecasts
            WHERE area_code = ?
            ORDER BY forecast_date
            """, (AREA_CODE,))

        rows = cur.fetchall()
        conn.close()

        if rows:
            output.value = "\n\n".join(
                [f"{d}\n{w}" for d, w in rows]
            )
        else:
            output.value = "該当する天気予報がありません"

        page.update()

    # --- レイアウト ---
    page.add(
        title,
        ft.Row(
            [date_input],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.ElevatedButton("天気予報を取得", on_click=fetch_weather),
                ft.ElevatedButton("天気予報を表示", on_click=show_weather),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(),
        output
    )


ft.app(target=main)