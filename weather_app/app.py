import flet as ft
import sqlite3
import subprocess
import datetime

DB_NAME = "weather.db"
AREA_CODE = "130000"

WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]


def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.window_width = 700
    page.window_height = 550

    title = ft.Text("天気予報アプリ", size=24, weight="bold")

    date_input = ft.TextField(
        label="日付指定（例: 2026-01-13）※空欄で週間表示",
        width=320
    )

    today_column = ft.Column()
    week_row = ft.Row(scroll=ft.ScrollMode.AUTO)

    # --- 天気取得 ---
    def fetch_weather(e):
        subprocess.run(["python", "fetch_weather.py"])
        today_column.controls.clear()
        week_row.controls.clear()
        today_column.controls.append(ft.Text("天気予報を取得しました", italic=True))
        page.update()

    # --- 天気表示 ---
    def show_weather(e):
        today_column.controls.clear()
        week_row.controls.clear()

        today = datetime.date.today().isoformat()

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute("""
        SELECT forecast_date, weather
        FROM weather_forecasts
        WHERE area_code = ?
        ORDER BY forecast_date
        """, (AREA_CODE,))

        rows = cur.fetchall()
        conn.close()

        for d, w in rows:
            date_str = d[:10]
            date_obj = datetime.date.fromisoformat(date_str)
            weekday = WEEKDAYS[date_obj.weekday()]

            # --- 絵文字 ---
            emoji = ""
            if "雨" in w:
                emoji = " ☔️"
            elif "晴" in w:
                emoji = " ☀️"

            is_today = date_str == today
            border_width = 3 if is_today else 1

            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"{date_str}（{weekday}）", weight="bold"),
                            ft.Text(f"{w}{emoji}")
                        ],
                        spacing=6
                    ),
                    padding=15,
                    width=180,
                    border=ft.border.all(border_width),
                    border_radius=10,
                )
            )

            if is_today:
                today_column.controls.append(
                    ft.Text("今日の天気", size=18, weight="bold")
                )
                today_column.controls.append(card)
            else:
                week_row.controls.append(card)

        page.update()

    page.add(
        title,
        ft.Row([date_input], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(
            [
                ft.ElevatedButton("天気予報を取得", on_click=fetch_weather),
                ft.ElevatedButton("天気予報を表示", on_click=show_weather),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(),
        today_column,
        ft.Text("週間天気", size=18, weight="bold"),
        week_row,
    )


ft.app(target=main)