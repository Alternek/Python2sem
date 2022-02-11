"""
Лабораторная работа 1: Калькулятор систем счисления
Вариант 23 (3)
ИУ7-26Б
Яремчук Иван
"""


from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout


class MainUi(QMainWindow):
    """
    Main GUI
    """
    def __init__(self):
        """
        GUI initializer
        """
        super().__init__()

        # Set main GUI properties
        self.setWindowTitle('Calculator')
        self.setFixedSize(300, 400)
        self.displayHeight = 40
        self.buttonsSize = (60, 60)

        # Set central widgets and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Create the displays and the buttons
        self._create_displays()
        self._create_buttons()

    def _create_displays(self):
        """
        Create decDisplay and terDisplay
        """
        # Decimal number
        self.decDisplay = QLineEdit()
        self.decDisplay.setMaxLength(30)
        self.decDisplay.setPlaceholderText("Enter decimal number")
        self.decDisplay.setFixedHeight(self.displayHeight)
        self.generalLayout.addWidget(self.decDisplay)

        # Ternary number
        self.terDisplay = QLineEdit()
        self.terDisplay.setMaxLength(30)
        self.terDisplay.setPlaceholderText("Enter ternary number")
        self.terDisplay.setFixedHeight(self.displayHeight)
        self.generalLayout.addWidget(self.terDisplay)

    def _create_buttons(self):
        """
        Create the buttons
        """
        self.buttons = {}
        buttons_layout = QGridLayout()
        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '+': (3, 0),
                   '0': (3, 1),
                   '-': (3, 2),
                   }

        # Add buttons to layout
        for btnName, position in buttons.items():
            self.buttons[btnName] = QPushButton(btnName)
            self.buttons[btnName].setFixedSize(*self.buttonsSize)
            buttons_layout.addWidget(self.buttons[btnName], position[0], position[1])

        # Add buttons_layout to generalLayout
        self.generalLayout.addLayout(buttons_layout)

    def set_dec_display_text(self, text):
        """
        Set text to decDisplay
        """
        self.decDisplay.setText(text)


app = QApplication([])
window = MainUi()
window.show()

app.exec()
