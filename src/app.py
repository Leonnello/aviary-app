from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic

import sys


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self = uic.loadUi("QtGUI/login.ui", self)
        
        self.test_button.clicked.connect(self.on_login)

    def on_login(self):
        # insert login validation here

        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self = uic.loadUi("QtGUI/form.ui", self)
        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())