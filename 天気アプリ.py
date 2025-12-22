import flet as ft
import requests

def main(page: ft.Page):
    page.title = "全国一週間天気予報（完全版）"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0

    TELOP_DICT = {
        "100": ["晴れ", "sunny", "orange"],
        "101": ["晴時々曇", "wb_sunny_outlined", "orange"],
        "200": ["曇り", "wb_cloudy", "grey"],
        "201": ["曇時々晴", "wb_cloudy_outlined", "grey"],
        "300": ["雨", "umbrella", "blue"],
        "400": ["雪", "ac_unit", "cyan"],
    }

    weather_grid = ft.Row(wrap=True, spacing=20, scroll="always", expand=True)

    def update_weather(area_code, area_name):
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        data = requests.get(url).json()
        
        short_weathers = data[0]["timeSeries"][0]["areas"][0]["weathers"]
        weekly_series = data[1]["timeSeries"]
        dates = weekly_series[0]["timeDefines"]
        weather_codes = weekly_series[0]["areas"][0]["weatherCodes"]
        temp_max = weekly_series[1]["areas"][0]["tempsMax"]
        temp_min = weekly_series[1]["areas"][0]["tempsMin"]

        weather_grid.controls.clear()
        
        for i in range(len(dates)):
            if i < len(short_weathers):
                weather_text = short_weathers[i]
                icon_name = "wb_sunny" if "晴" in weather_text else "wb_cloudy"
                icon_color = "orange" if "晴" in weather_text else "blue"
            else:
                code = weather_codes[i]
                info = TELOP_DICT.get(code, ["曇り", "wb_cloudy", "blue"])
                weather_text = info[0]
                icon_name = info[1]
                icon_color = info[2]

            high = temp_max[i] if i < len(temp_max) and temp_max[i] != "" else "--"
            low = temp_min[i] if i < len(temp_min) and temp_min[i] != "" else "--"

            weather_grid.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(dates[i][:10].replace("-", "/"), weight="bold"),
                            ft.Icon(name=icon_name, color=icon_color, size=40),
                            ft.Text(weather_text, size=11, text_align="center", height=35),
                            ft.Row([
                                ft.Text(f"{low}°", color="blue", weight="bold"),
                                ft.Text("/", color="grey"),
                                ft.Text(f"{high}°", color="red", weight="bold"),
                            ], alignment="center"),
                        ], horizontal_alignment="center"),
                        padding=15, width=140
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
                leading=ft.Icon("location_on"),
                title=ft.Text(info["name"]),
                on_click=lambda e, c=code, n=info["name"]: update_weather(c, n)
            )
        )

    header = ft.Container(
        content=ft.Text("全国一週間天気予報", color="white", size=20, weight="bold"),
        bgcolor="#311b92",
        padding=15,
        width=page.width,
    )

    page.add(
        header,
        ft.Row([
            ft.Container(content=region_list_view, width=200, bgcolor="#f5f5f5"),
            ft.VerticalDivider(width=1),
            ft.Container(content=weather_grid, padding=20, expand=True)
        ], expand=True)
    )

    update_weather("130000", "東京都")

ft.app(target=main)