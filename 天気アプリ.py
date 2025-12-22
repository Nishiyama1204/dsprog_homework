import flet as ft
import requests

def main(page: ft.Page):
    page.title = "天気予報アプリ"

    weather_text = ft.Text(value="地域を選んでください", size=20)
    
    region_dropdown = ft.Dropdown(
        label="地域を選択",
        width=300,
        options=[]
    )

    def display_weather(e):
        if region_dropdown.value is None:
            weather_text.value = "地域を選択してください！"
        else:
            code = region_dropdown.value
            url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
            
            data = requests.get(url).json()
            forecast = data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
            
            weather_text.value = f"選択した地域の天気: {forecast}"
        page.update()

    def load_regions():
        url = "http://www.jma.go.jp/bosai/common/const/area.json"
        response = requests.get(url).json()
        
        offices = response["offices"]
        
        for code, info in offices.items():
            region_dropdown.options.append(
                ft.dropdown.Option(key=code, text=info["name"])
            )
        page.update()

    page.add(
        region_dropdown,
        ft.ElevatedButton("天気を表示", on_click=display_weather),
        weather_text
    )

    load_regions()

ft.app(target=main)