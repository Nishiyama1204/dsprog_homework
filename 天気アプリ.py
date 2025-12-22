import flet as ft
import requests

def main(page: ft.Page):
    page.title = "全国天気予報アプリ"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    weather_grid = ft.Row(wrap=True, spacing=20, scroll="always", expand=True)

    def update_weather(area_code, area_name):
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        data = requests.get(url).json()
        
        time_series_w = data[0]["timeSeries"][0]
        dates = time_series_w["timeDefines"]
        weathers = time_series_w["areas"][0]["weathers"]

        t_min_list = []
        t_max_list = []
        
        try:
            for ts in data:
                for entry in ts["timeSeries"]:
                    areas = entry["areas"][0]
                    if "temps" in areas:
                        temps = areas["temps"]
                        for i in range(0, len(temps), 2):
                            t_min_list.append(temps[i])
                            if i+1 < len(temps):
                                t_max_list.append(temps[i+1])
                    elif "tempsMax" in areas:
                        t_max_list = areas["tempsMax"]
                        t_min_list = areas["tempsMin"]
        except:
            pass

        weather_grid.controls.clear()
        weather_grid.controls.append(
            ft.Container(
                content=ft.Text(f"{area_name}の天気予報", size=30, weight="bold", color="#311b92"),
                width=1000, padding=ft.padding.only(bottom=10)
            )
        )
        
        for i in range(len(weathers)):
            high = t_max_list[i] if i < len(t_max_list) and t_max_list[i] != "" else "--"
            low = t_min_list[i] if i < len(t_min_list) and t_min_list[i] != "" else "--"

            weather_grid.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(dates[i][:10].replace("-", "/"), weight="bold", size=16),
                            ft.Icon(name="wb_sunny", color="orange", size=50),
                            ft.Text(weathers[i], size=14, text_align="center", weight="w500"),
                            ft.Container(height=5),
                            ft.Row([
                                ft.Text(f"{low}°", color="blue", weight="bold", size=20),
                                ft.Text("/", color="grey", size=20),
                                ft.Text(f"{high}°", color="red", weight="bold", size=20),
                            ], alignment="center"),
                        ], horizontal_alignment="center"),
                        padding=20, width=200, height=220
                    )
                )
            )
        page.update()

    region_list_view = ft.ListView(expand=True, spacing=5)
    url_area = "http://www.jma.go.jp/bosai/common/const/area.json"
    offices = requests.get(url_area).json()["offices"]

    for code, info in offices.items():
        region_list_view.controls.append(
            ft.ListTile(
                leading=ft.Icon("location_on", color="#546e7a"),
                title=ft.Text(info["name"], weight="bold"),
                on_click=lambda e, c=code, n=info["name"]: update_weather(c, n)
            )
        )

    page.add(
        ft.Row([
            ft.Container(content=region_list_view, width=250, bgcolor="#f5f5f5"),
            ft.VerticalDivider(width=1),
            ft.Container(content=weather_grid, padding=30, expand=True)
        ], expand=True)
    )

    update_weather("130000", "東京都")

ft.app(target=main)