import flet as ft
import requests

def main(page: ft.Page):
    page.title = "天気予報アプリ（試作）"
    
    # 1. 天気を表示するための文字（Text）を用意
    weather_text = ft.Text(value="ここに結果が出ます", size=20)

    # 2. ボタンを押した時の動きを決める
    def get_weather(e):
        # 東京のデータを取ってくる
        url = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"
        data = requests.get(url).json()
        
        # データの深いところにある「天気情報」を取り出す（ここは少し難しいけど決まり文句）
        forecast = data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
        
        # 画面の文字を書き換えて、更新（update）する
        weather_text.value = f"東京の天気: {forecast}"
        page.update()

    # 3. 画面に部品（ボタンとテキスト）を置く
    page.add(
        ft.ElevatedButton("東京の天気を取得", on_click=get_weather),
        weather_text
    )

ft.app(target=main)