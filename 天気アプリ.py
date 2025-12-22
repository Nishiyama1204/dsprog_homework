import flet as ft
import requests

def main(page: ft.Page):
    page.title = "天気予報アプリ"

    # --- 部品の設定 ---
    # 1. 天気を表示するテキスト
    weather_text = ft.Text(value="地域を選んでください", size=20)
    
    # 2. 地域を選ぶメニュー（Dropdown）
    region_dropdown = ft.Dropdown(
        label="地域を選択",
        width=300,
        options=[] # 最初は空っぽ
    )

    # --- 動きの設定 ---
    # ボタンが押された時の処理
    def display_weather(e):
        if region_dropdown.value is None:
            weather_text.value = "地域を選択してください！"
        else:
            # 選択された地域の番号を使ってURLを作る
            code = region_dropdown.value
            url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
            
            data = requests.get(url).json()
            forecast = data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
            
            weather_text.value = f"選択した地域の天気: {forecast}"
        page.update()

    # --- 最初の準備（地域の名簿を読み込む） ---
    def load_regions():
        # スライド1枚目のURL
        url = "http://www.jma.go.jp/bosai/common/const/area.json"
        response = requests.get(url).json()
        
        # 「offices」という項目の中に地域名と番号が入っています
        offices = response["offices"]
        
        for code, info in offices.items():
            # メニューに「地域の名前」を追加し、裏側で「番号」を保持する
            region_dropdown.options.append(
                ft.dropdown.Option(key=code, text=info["name"])
            )
        page.update()

    # --- 画面を作る ---
    page.add(
        region_dropdown,
        ft.ElevatedButton("天気を表示", on_click=display_weather),
        weather_text
    )

    # アプリ起動時に地域リストを読み込む
    load_regions()

ft.app(target=main)