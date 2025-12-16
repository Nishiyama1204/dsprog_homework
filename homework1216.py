import flet as ft
import math 


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


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


class ScientificButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.DEEP_ORANGE_700 
        self.color = ft.Colors.WHITE


class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)
        self.width = 500
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        
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
                    ScientificButton(text="1/x", button_clicked=self.scientific_button_clicked),
                    ft.Container(expand=1), 
                    ft.Container(expand=1),
                    ft.Container(expand=1),
                ]
            ),
        ]

        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                *self.scientific_rows,
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
        data = e.control.data
        print(f"Button clicked with data = {data}")
        
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()
        
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            current_value = self.result.value
            
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
                pass
            else:
                if len(current_value) < 16:
                    self.result.value += data

        elif data in ("+", "-", "×", "÷"): 
            try:
                self.result.value = self.calculate(self.operand1, float(self.result.value), self.operator)
                self.operator = data
                
                if self.result.value == "Error":
                    self.operand1 = 0
                else:
                    self.operand1 = float(self.result.value)
                self.new_operand = True
            except ValueError:
                 self.result.value = "Error"
                 self.reset()

        elif data in ("="):
            self.result.value = self.calculate(self.operand1, float(self.result.value), self.operator)
            self.reset()

        elif data in ("%"):
            try:
                self.result.value = self.format_number(float(self.result.value) / 100)
                self.new_operand = True
            except ValueError:
                self.result.value = "Error"
                self.reset()

        elif data in ("+/-"):
            try:
                current_value = float(self.result.value)
                self.result.value = self.format_number(-current_value)
            except ValueError:
                self.result.value = "Error"
                self.reset()

        self.update()

    def scientific_button_clicked(self, e):
        data = e.control.data
        print(f"Scientific Button clicked with data = {data}")

        if self.result.value == "Error":
            return

        try:
            value = float(self.result.value)
            result = None

            if data == "sin":
                result = math.sin(math.radians(value)) 
            elif data == "cos":
                result = math.cos(math.radians(value))
            elif data == "tan":
                if value % 90 == 0 and value % 180 != 0:
                    self.result.value = "Error"
                    self.reset()
                    self.update()
                    return
                result = math.tan(math.radians(value))
            elif data == "log":
                if value <= 0:
                    self.result.value = "Error"
                    self.reset()
                    self.update()
                    return
                result = math.log10(value)
            elif data == "ln":
                if value <= 0:
                    self.result.value = "Error"
                    self.reset()
                    self.update()
                    return
                result = math.log(value)
            elif data == "√":
                if value < 0:
                    self.result.value = "Error"
                    self.reset()
                    self.update()
                    return
                result = math.sqrt(value)
            elif data == "1/x":
                if value == 0:
                    self.result.value = "Error"
                    self.reset()
                    self.update()
                    return
                result = 1 / value
            
            if result is not None:
                self.result.value = self.format_number(result)
                self.new_operand = True
            
        except ValueError:
            self.result.value = "Error"
            self.reset()
        
        self.update()

    def format_number(self, num):
        if num is None:
            return "0"
        
        if abs(num - round(num)) < 1e-9:
            return int(round(num))
        else:
            return float(f"{num:.10f}")

    def calculate(self, operand1, operand2, operator):

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
        
        return self.format_number(operand2)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Scientific Calculator (Flet)"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK 
    calc = CalculatorApp()
    page.add(calc)


ft.app(target=main)