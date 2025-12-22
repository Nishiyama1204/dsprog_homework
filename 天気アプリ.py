import flet as ft
import requests

def main(page: ft.Page):
    page.title = "天気予報アプリ（試作）"

    weather_text = ft.Text(value="ここに結果が出ます", size=20)

    def get_weather(e):
        url = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"
        data = requests.get(url).json()

        forecast = data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
        
        weather_text.value = f"東京の天気: {forecast}"
        page.update()

    page.add(
        ft.ElevatedButton("東京の天気を取得", on_click=get_weather),
        weather_text
    )

ft.app(target=main)