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
        
        time_series = data[0]["timeSeries"][0]
        dates = time_series["timeDefines"]
        weathers = time_series["areas"][0]["weathers"]

        weather_grid.controls.clear()
        weather_grid.controls.append(ft.Text(f"{area_name}の予報", size=25, weight="bold", width=1000))
        
        for i in range(len(weathers)):
            weather_grid.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(dates[i][:10], weight="bold"),
                            ft.Icon(name="wb_sunny", color="orange", size=40),
                            ft.Text(weathers[i], size=12, text_align="center"),
                        ], horizontal_alignment="center"),
                        padding=20, width=160
                    )
                )
            )
        page.update()

    region_list_view = ft.ListView(expand=True, spacing=10, padding=10)

    url_area = "http://www.jma.go.jp/bosai/common/const/area.json"
    area_data = requests.get(url_area).json()
    offices = area_data["offices"]

    for code, info in offices.items():
        region_list_view.controls.append(
            ft.ListTile(
                leading=ft.Icon("location_on"),
                title=ft.Text(info["name"]),
                on_click=lambda e, c=code, n=info["name"]: update_weather(c, n)
            )
        )

    page.add(
        ft.Row([
            ft.Container(
                content=region_list_view,
                width=250,
                bgcolor="#f5f5f5",
            ),
            ft.VerticalDivider(width=1),
            ft.Container(
                content=weather_grid,
                padding=20,
                expand=True
            )
        ], expand=True)
    )

    update_weather("130000", "東京都")

ft.app(target=main)