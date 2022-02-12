"""
Лабораторная работа 1: Калькулятор систем счисления
Вариант 23 (3)
ИУ7-26Б
Яремчук Иван
"""


from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout, \
    QComboBox


class Calculator:
    """
    Decimal <-> ternary calculator
    """

    @staticmethod
    def select_symbols(text: str, number_type: str) -> str:
        """
        Select correct symbols
        """
        if number_type == "decimal":
            return ''.join([symbol for symbol in text if symbol in "0123456789"]).lstrip('0')
        else:
            return ''.join([symbol for symbol in text if symbol in "0+-"]).lstrip('0')

    @staticmethod
    def to_dec(number: str) -> str:
        """
        Convert dec to ter
        """
        alphabet = {"-": -1, "0": 0, "+": 1}
        number = number[::-1]
        dec_number = 0
        exp = 0
        for symbol in number:
            dec_number += alphabet[symbol] * 3 ** exp
            exp += 1
        return str(dec_number).lstrip('0')

    @staticmethod
    def to_ter(number: str) -> str:
        """
        Convert ter to dec
        """
        ter_number = ""
        number = int(number)
        while number:
            ter_number = "0+-"[number % 3] + ter_number  # left append
            number = (number + 1) // 3  # floor divide
        return ter_number.lstrip('0')


class MainUi(QMainWindow):
    """
    Main GUI
    """
    def __init__(self):
        """
        GUI initializer
        """
        super().__init__()

        # Set fields
        self.displayHeight = 40
        self.buttonsSize = (60, 60)
        self.windowSize = (300, 500)

        # Set main GUI properties
        self.setWindowTitle('Calculator')
        self.setFixedSize(*self.windowSize)

        # Set central widgets and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Create the displays and the buttons
        self._create_displays()
        self._create_switch()
        self._create_buttons()
        self._create_menubar()

        self._switch_active_display(0)

        # Create connections with buttons and LineEdits
        for button_name in self.buttons:
            self.buttons[button_name].clicked.connect(self._generate_button(button_name))
        self.decDisplay.editingFinished.connect(self._change_ternary)
        self.terDisplay.editingFinished.connect(self._change_decimal)

    def _create_displays(self) -> None:
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

    def _create_switch(self):
        """
        Create switchWidget
        """
        self.switchWidget = QComboBox()
        self.switchWidget.addItems(["Decimal", "Ternary"])
        self.switchWidget.currentIndexChanged.connect(self._switch_active_display)
        self.generalLayout.addWidget(self.switchWidget)

    def _create_buttons(self) -> None:
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
                   'CE': (4, 2)
                   }

        # Add buttons to layout
        for btnName, position in buttons.items():
            self.buttons[btnName] = QPushButton(btnName)
            self.buttons[btnName].setFixedSize(*self.buttonsSize)
            buttons_layout.addWidget(self.buttons[btnName], position[0], position[1])

        # Add buttons_layout to generalLayout
        self.generalLayout.addLayout(buttons_layout)

    def _create_menubar(self):
        """
        Create menu
        """
        self.menubar = self.menuBar()
        self.editMenu = self.menubar.addMenu("Edit")
        self.helpMenu = self.menubar.addMenu("Help")

    def _switch_active_display(self, index: int) -> None:
        if index == 0:
            self.activeDisplay = self.decDisplay
            for button in "+-":
                self.buttons[button].setDisabled(True)
            for button in "0123456789":
                self.buttons[button].setDisabled(False)
        else:
            self.activeDisplay = self.terDisplay
            for button in "123456789":
                self.buttons[button].setDisabled(True)
            for button in "+0-":
                self.buttons[button].setDisabled(False)

    def _generate_button(self, name: str):
        """
        Generate function-buttons for connections
        """
        def button():
            if name == 'CE':
                self.clear_text()
            else:
                self.add_symbol(name)
        return button

    def _change_ternary(self):
        """
        Change ternary if decimal is modified
        """
        if self.decDisplay.text() in ['', '0']:
            self.decDisplay.setText('')
            self.terDisplay.setText('')
        if self.decDisplay.isModified():
            self.decDisplay.setText(Calculator.select_symbols(self.decDisplay.text(), "decimal"))
            self.terDisplay.setText(Calculator.to_ter(self.decDisplay.text()))

    def _change_decimal(self):
        """
        Change decimal if ternary is modified
        """
        if self.terDisplay.isModified():
            if self.terDisplay.text() in ['', '0']:
                self.decDisplay.setText('')
                self.terDisplay.setText('')
            self.terDisplay.setText(Calculator.select_symbols(self.terDisplay.text(), "ternary"))
            self.decDisplay.setText(Calculator.to_dec(self.terDisplay.text()))

    def set_text(self, text: str) -> None:
        """
        Set text to activeDisplay
        """
        self.activeDisplay.setText(text)
        self._synchronize_display()

    def get_text(self) -> str:
        """
        Get text from activeDisplay
        """
        return self.activeDisplay.text()

    def add_symbol(self, text: str) -> None:
        """
        Add symbol to activeDisplay
        """
        if self.activeDisplay == self.decDisplay:
            if text in "0123456789":
                self.set_text(self.get_text() + text)
        else:
            if text in "+-0":
                self.set_text(self.get_text() + text)
        self._synchronize_display()

    def del_symbol(self) -> None:
        """
        Delete symbol from activeDisplay
        """
        if len(self.get_text()):
            self.set_text(self.get_text()[:-1])
            self._synchronize_display()

    def clear_text(self):
        """
        Clear text
        """
        self.decDisplay.setText('')
        self.terDisplay.setText('')

    def _synchronize_display(self) -> None:
        """
        Synchronize terDisplay and DecDisplay
        """
        if self.activeDisplay == self.decDisplay:
            self.terDisplay.setText(Calculator.to_ter(self.get_text()))
        else:
            self.decDisplay.setText(Calculator.to_dec(self.get_text()))


# Create App and GUI
app = QApplication([])
window = MainUi()

# Execution
window.show()
app.exec()
