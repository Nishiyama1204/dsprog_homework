import flet as ft
import requests

def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0

    weather_grid = ft.Row(wrap=True, spacing=20, scroll="always", expand=True)

    def update_weather(area_code):
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        data = requests.get(url).json()
        
        time_series = data[0]["timeSeries"][0]
        dates = time_series["timeDefines"]
        weathers = time_series["areas"][0]["weathers"]

        weather_grid.controls.clear()

        for i in range(len(weathers)):
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(dates[i][:10], size=14, weight="bold"),
                        ft.Icon(name="sunny", color="orange", size=40), 
                        ft.Text(weathers[i], size=12, text_align="center"),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20, width=150,
                )
            )
            weather_grid.controls.append(card)
        page.update()

    regions = [
        {"name": "東京都", "code": "130000"},
        {"name": "茨城県", "code": "080000"},
        {"name": "千葉県", "code": "120000"},
        {"name": "北海道", "code": "010100"},
    ]

    def on_rail_change(e):
        idx = e.control.selected_index
        update_weather(regions[idx]["code"])

    rail = ft.NavigationRail(
        selected_index=0,
        label_type="all",
        min_width=100,
        bgcolor="#eeeeee",
        destinations=[
            ft.NavigationRailDestination(icon="location_on", label=r["name"]) for r in regions
        ],
        on_change=on_rail_change
    )

    page.add(
        ft.Row([
            rail,
            ft.VerticalDivider(width=1),
            ft.Container(content=weather_grid, padding=20, expand=True)
        ], expand=True)
    )

    update_weather("130000")

ft.app(target=main)