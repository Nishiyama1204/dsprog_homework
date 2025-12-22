import flet as ft
import requests

def main(page: ft.Page):
    page.title = "全国一週間天気予報"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0

    TELOP_DICT = {
        "100": ["晴れ", "wb_sunny", "orange"],
        "101": ["晴時々曇", "wb_sunny_outlined", "orange"],
        "200": ["曇り", "wb_cloudy", "blue-grey"],
        "201": ["曇時々晴", "wb_cloudy_outlined", "blue-grey"],
        "300": ["雨", "umbrella", "blue"],
        "400": ["雪", "ac_unit", "cyan"],
    }

    weather_grid = ft.Row(wrap=True, spacing=20, scroll="always", expand=True)
    weather_container = ft.Container(
        content=weather_grid,
        padding=30,
        expand=True,
        bgcolor="#e3f2fd"
    )

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
        
        weather_grid.controls.append(
            ft.Container(
                content=ft.Text(f"{area_name}の週間予報", size=28, weight="bold", color="#1a237e"),
                width=2000
            )
        )
        
        for i in range(len(dates)):
            if i < len(short_weathers):
                weather_text = short_weathers[i]
                icon_name = "wb_sunny" if "晴" in weather_text else "wb_cloudy"
                icon_color = "orange" if "晴" in weather_text else "blue"
            else:
                code = weather_codes[i]
                info = TELOP_DICT.get(code, ["曇り", "wb_cloudy", "blue-grey"])
                weather_text = info[0]
                icon_name = info[1]
                icon_color = info[2]

            high = temp_max[i] if i < len(temp_max) and temp_max[i] != "" else "--"
            low = temp_min[i] if i < len(temp_min) and temp_min[i] != "" else "--"

            weather_grid.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(dates[i][:10].replace("-", "/"), weight="bold", size=15),
                            ft.Icon(name=icon_name, color=icon_color, size=45),
                            ft.Text(weather_text, size=12, text_align="center", height=35),
                            ft.Row([
                                ft.Text(f"{low}°", color="blue", weight="bold", size=18),
                                ft.Text("/", color="grey"),
                                ft.Text(f"{high}°", color="red", weight="bold", size=18),
                            ], alignment="center"),
                        ], horizontal_alignment="center"),
                        padding=20, width=160, bgcolor="white"
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
        content=ft.Text("全国天気予報アプリ", color="white", size=22, weight="bold"),
        bgcolor="#1a237e",
        padding=20,
        alignment=ft.alignment.center_left,
        width=float("inf"),
    )

    page.add(
        header,
        ft.Row([
            ft.Container(content=region_list_view, width=250, bgcolor="#f5f5f5"),
            ft.VerticalDivider(width=1),
            weather_container 
        ], expand=True)
    )

    update_weather("130000", "東京都")

ft.app(target=main)