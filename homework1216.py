import flet as ft
import math 


# --- Button Base Classes ---

class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text # クリックされたボタンのテキストをデータとして保持


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.Colors.WHITE24
        self.color = ft.Colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.ORANGE
        self.color = ft.Colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.BLUE_GREY_100
        self.color = ft.Colors.BLACK

# 科学計算ボタン用のクラス（見た目を区別）
class ScientificButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.DEEP_ORANGE_700 
        self.color = ft.Colors.WHITE


# --- Calculator Application Class ---

class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)
        self.width = 500 # 科学計算モード用に幅を拡大
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        
        # 科学計算ボタンのレイアウト
        self.scientific_rows = [
            ft.Row(
                controls=[
                    ScientificButton(text="sin", button_clicked=self.scientific_button_clicked),
                    ScientificButton(text="cos", button_clicked=self.scientific_button_clicked),
                    ScientificButton(text="tan", button_clicked=self.scientific_button_clicked),
                    ScientificButton(text="log", button_clicked=self.scientific_button_clicked),
                    ScientificButton(text="ln", button_clicked=self.scientific_button_clicked),
                ]
            ),
            ft.Row(
                controls=[
                    ScientificButton(text="√", button_clicked=self.scientific_button_clicked),
                    # x^y は2項演算なので、既存のbutton_clickedを呼び出す
                    ScientificButton(text="$x^y$", button_clicked=self.button_clicked), 
                    ScientificButton(text="$x^2$", button_clicked=self.scientific_button_clicked),
                    ScientificButton(text="$e^x$", button_clicked=self.scientific_button_clicked),
                    ScientificButton(text="1/x", button_clicked=self.scientific_button_clicked),
                ]
            ),
        ]

        # メインコンテンツのレイアウト
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                *self.scientific_rows, # 科学計算ボタンの行を挿入
                ft.Row(
                    controls=[
                        ExtraActionButton(text="AC", button_clicked=self.button_clicked),
                        ExtraActionButton(text="+/-", button_clicked=self.button_clicked),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="÷", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="×", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="0", expand=2, button_clicked=self.button_clicked),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        """標準の数字、小数点、四則演算、AC、=、+/-、%を処理"""
        data = e.control.data
        print(f"Button clicked with data = {data}")
        
        # エラー表示からのリセットまたはAC
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()
        
        # 数字と小数点
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            current_value = self.result.value
            
            # 画面が"0"か新しいオペランド入力時、または"."が押された時
            if current_value == "0" or self.new_operand:
                if data == ".":
                    if self.new_operand:
                        self.result.value = "0."
                    elif "." not in current_value:
                        self.result.value += "."
                else:
                    self.result.value = data
                    self.new_operand = False
            elif "." in data and "." in current_value:
                # 既に"."がある場合は何もしない
                pass
            else:
                if len(current_value) < 16: # 表示桁数制限（任意）
                    self.result.value += data

        # 2項演算子（四則演算 + 累乗 $x^y$）
        elif data in ("+", "-", "×", "÷", "$x^y$"): 
            try:
                # 既に保持しているオペランドと現在の値を計算
                self.result.value = self.calculate(self.operand1, float(self.result.value), self.operator)
                self.operator = data
                
                # 計算結果を次のオペランド1として保持
                if self.result.value == "Error":
                    self.operand1 = 0
                else:
                    self.operand1 = float(self.result.value)
                self.new_operand = True
            except ValueError:
                 self.result.value = "Error"
                 self.reset()

        # 等号
        elif data in ("="):
            self.result.value = self.calculate(self.operand1, float(self.result.value), self.operator)
            self.reset()

        # パーセント
        elif data in ("%"):
            try:
                self.result.value = self.format_number(float(self.result.value) / 100)
                self.new_operand = True
            except ValueError:
                self.result.value = "Error"
                self.reset()

        # +/-符号反転
        elif data in ("+/-"):
            try:
                current_value = float(self.result.value)
                self.result.value = self.format_number(-current_value)
            except ValueError:
                self.result.value = "Error"
                self.reset()

        self.update()

    def scientific_button_clicked(self, e):
        """科学計算モードの単項演算子を処理するハンドラ"""
        data = e.control.data
        print(f"Scientific Button clicked with data = {data}")

        if self.result.value == "Error":
            return

        try:
            value = float(self.result.value)
            result = None

            if data == "sin":
                # 度をラジアンに変換して計算
                result = math.sin(math.radians(value)) 
            elif data == "cos":
                result = math.cos(math.radians(value))
            elif data == "tan":
                # 90度や270度付近での発散を防ぐための簡単なチェック
                if value % 90 == 0 and value % 180 != 0:
                    self.result.value = "Error"
                    self.reset()
                    self.update()
                    return
                result = math.tan(math.radians(value))
            elif data == "log": # 常用対数 (log10)
                if value <= 0:
                    self.result.value = "Error"
                    self.reset()
                    self.update()
                    return
                result = math.log10(value)
            elif data == "ln": # 自然対数 (log e)
                if value <= 0:
                    self.result.value = "Error"
                    self.reset()
                    self.update()
                    return
                result = math.log(value)
            elif data == "√": # 平方根
                if value < 0:
                    self.result.value = "Error"
                    self.reset()
                    self.update()
                    return
                result = math.sqrt(value)
            elif data == "$x^2$": # 2乗
                result = value ** 2
            elif data == "$e^x$": # eのx乗
                result = math.exp(value)
            elif data == "1/x": # 逆数
                if value == 0:
                    self.result.value = "Error"
                    self.reset()
                    self.update()
                    return
                result = 1 / value
            
            # 結果を画面に反映
            if result is not None:
                self.result.value = self.format_number(result)
                self.new_operand = True
            
        except ValueError:
            self.result.value = "Error"
            self.reset()
        
        self.update()

    def format_number(self, num):
        """結果を整数または適切な浮動小数点形式にフォーマット"""
        if num is None:
            return "0"
        
        # 浮動小数点誤差を考慮し、ほぼ整数ならintに変換
        if abs(num - round(num)) < 1e-9:
            return int(round(num))
        else:
            # 表示桁数を制限する（例：小数点以下10桁）
            return float(f"{num:.10f}")

    def calculate(self, operand1, operand2, operator):
        """2つのオペランドとオペレータに基づいて計算を実行"""

        if operator == "+":
            return self.format_number(operand1 + operand2)

        elif operator == "-":
            return self.format_number(operand1 - operand2)

        elif operator == "×":
            return self.format_number(operand1 * operand2)

        elif operator == "÷":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)
        
        elif operator == "$x^y$": # 累乗の処理
            return self.format_number(operand1 ** operand2)

        return self.format_number(operand2) # オペレータが未設定の場合は現在の値を返す

    def reset(self):
        """電卓の状態を初期化"""
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Scientific Calculator (Flet)"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK # ダークモードに設定
    calc = CalculatorApp()
    page.add(calc)


ft.app(target=main)