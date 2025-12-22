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

    def update_weather(area_code, area_name):
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        data = requests.get(url).json()
        
        today_date = data[0]["timeSeries"][0]["timeDefines"][0]
        today_weather = data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
        
        weekly_series = data[1]["timeSeries"]
        weekly_dates = weekly_series[0]["timeDefines"]
        weather_codes = weekly_series[0]["areas"][0]["weatherCodes"]
        temp_max = weekly_series[1]["areas"][0]["tempsMax"]
        temp_min = weekly_series[1]["areas"][0]["tempsMin"]

        weather_grid.controls.clear()
        
        weather_grid.controls.append(
            ft.Container(
                content=ft.Text(f"{area_name}の天気予報", size=28, weight="bold", color="#1a237e"),
                width=2000
            )
        )

        today_high = "--"
        today_low = "--"
        try:
            for ts in data[0]["timeSeries"]:
                if "temps" in ts["areas"][0]:
                    t_list = ts["areas"][0]["temps"]
                    if len(t_list) >= 2:
                        today_low, today_high = t_list[0], t_list[1]
                    break
        except: pass

        weather_grid.controls.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("今日 " + today_date[:10].replace("-", "/"), weight="bold", color="red"),
                        ft.Icon(name="wb_sunny" if "晴" in today_weather else "wb_cloudy", 
                                color="orange" if "晴" in today_weather else "blue", size=45),
                        ft.Text(today_weather, size=12, text_align="center", height=35),
                        ft.Row([
                            ft.Text(f"{today_low}°", color="blue", weight="bold"),
                            ft.Text("/"),
                            ft.Text(f"{today_high}°", color="red", weight="bold")
                        ], alignment="center"),
                    ], horizontal_alignment="center"),
                    padding=20, width=160, bgcolor="white"
                )
            )
        )

        for i in range(len(weekly_dates)):
            code = weather_codes[i]
            info = TELOP_DICT.get(code, ["曇り", "wb_cloudy", "blue-grey"])
            high = temp_max[i] if i < len(temp_max) and temp_max[i] != "" else "--"
            low = temp_min[i] if i < len(temp_min) and temp_min[i] != "" else "--"

            weather_grid.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(weekly_dates[i][:10].replace("-", "/"), weight="bold"),
                            ft.Icon(name=info[1], color=info[2], size=45),
                            ft.Text(info[0], size=12, text_align="center", height=35),
                            ft.Row([
                                ft.Text(f"{low}°", color="blue", weight="bold"),
                                ft.Text("/"),
                                ft.Text(f"{high}°", color="red", weight="bold")
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
                title=ft.Text(info["name"]),
                on_click=lambda e, c=code, n=info["name"]: update_weather(c, n)
            )
        )

    header = ft.Container(
        content=ft.Text("全国天気予報アプリ", color="white", size=22, weight="bold"),
        bgcolor="#1a237e",
        padding=20,
        width=float("inf")
    )

    page.add(
        header,
        ft.Row([
            ft.Container(content=region_list_view, width=250, bgcolor="#f5f5f5"),
            ft.VerticalDivider(width=1),
            ft.Container(content=weather_grid, padding=30, expand=True, bgcolor="#e3f2fd")
        ], expand=True)
    )

    update_weather("130000", "東京都")

ft.app(target=main)