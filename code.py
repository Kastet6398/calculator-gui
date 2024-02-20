import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import requests

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.expression_label = QLabel('Enter expression:')
        self.expression_input = QLineEdit()
        self.expression_input.setClearButtonEnabled(True)
        self.result_label = QLabel('Result:')

        buttons_layout = QVBoxLayout()

        buttons = [
            ['7', '8', '9', '/', 'pi', '(',     'j',    'i',    'x',    'a',    'c',    ],
            ['4', '5', '6', '*', 'e',  ')',     '^',    'c',    'y',    'b',    'd',    ],
            ['1', '2', '3', '-', 'sin', 'tan',  'asin', 'atan', 'sinh', 'tanh', 'sinc', ],
            ['0', '.', '=', '+', 'cos', 'cot',  'acos', 'acot', 'cosh', 'coth', 'log',  ],
        ]

        for line in buttons:
            grid_layout = QHBoxLayout()
            for button_text in line:
                button = QPushButton(button_text)
                button.clicked.connect(lambda ttext=button_text: (print(button_text),self.handle_button_click(ttext)))
                grid_layout.addWidget(button)

            buttons_layout.addLayout(grid_layout)


        main_layout = QVBoxLayout()
        main_layout.addWidget(self.expression_label)
        main_layout.addWidget(self.expression_input)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)

        self.setWindowTitle('Qt Calculator')
        self.show()

    def handle_button_click(self, button_text):
        QMessageBox.warning(self, 'Warning', str(button_text))

        if button_text == '=':
            self.calculate()
        else:
            current_text = self.expression_input.text()
            self.expression_input.setText(current_text + button_text)

    def calculate(self):
        expression = self.expression_input.text()

        url = 'https://py-learn.onrender.com/api/calculator/'
        data = {'expression': expression}

        response = requests.post(url, data=data)

        if response.status_code == 200:
            result = response.json()['result']
            self.result_label.setText(f'Result: {result}')
        else:
            error_message = f'Request failed. Status code: {response.status_code}\nResponse: {response.text}'
            self.result_label.setText(error_message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator_app = CalculatorApp()
    sys.exit(app.exec_())

