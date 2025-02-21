from PyQt6.QtWidgets import QApplication, QWidget, QHeaderView
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
        
        # connect navbar buttons
        self.navbar_account_button.clicked.connect(self.on_navbar_account_button_clicked)
        self.navbar_application_button.clicked.connect(self.on_navbar_application_button_clicked)
        self.navbar_archive_button.clicked.connect(self.on_navbar_archive_button_clicked)
        self.navbar_home_button.clicked.connect(self.on_navbar_home_button_clicked)
        self.navbar_logout_button.clicked.connect(self.on_navbar_logout_button_clicked)
        self.navbar_notif_button.clicked.connect(self.on_navbar_notif_button_clicked)

        # REVISE: move to separate function later
        # resize table cols to header/content
        self.application_table.resizeColumnsToContents()
        self.application_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

    #### Navbar Button Functions
    def on_navbar_account_button_clicked(self):
        self.current_tab.setCurrentIndex(0)
        
    def on_navbar_notif_button_clicked(self):
        self.current_tab.setCurrentIndex(1)
        
    def on_navbar_home_button_clicked(self):
        self.current_tab.setCurrentIndex(2)
    
    def on_navbar_application_button_clicked(self):
        self.current_tab.setCurrentIndex(3)
    
    def on_navbar_archive_button_clicked(self):
        self.current_tab.setCurrentIndex(4)

    def on_navbar_logout_button_clicked(self):
        # insert logout here
        pass
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())