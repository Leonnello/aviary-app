from PyQt6.QtWidgets import QApplication, QWidget, QHeaderView, QFrame
from PyQt6 import uic

import sys
import custom_gui_classes as custom


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
        
        # NOTE: Testing, remove later
        self.test_button.clicked.connect(self.on_applicant_selected_clicked)
        
        # connect navbar buttons
        self.navbar_account_button.clicked.connect(self.on_navbar_account_button_clicked)
        self.navbar_application_button.clicked.connect(self.on_navbar_application_button_clicked)
        self.navbar_archive_button.clicked.connect(self.on_navbar_archive_button_clicked)
        self.navbar_home_button.clicked.connect(self.on_navbar_home_button_clicked)
        self.navbar_logout_button.clicked.connect(self.on_navbar_logout_button_clicked)
        self.navbar_notif_button.clicked.connect(self.on_navbar_notif_button_clicked)
        
        # connect other buttons
        self.new_application_button.clicked.connect(self.on_new_application_button_clicked)
        self.profile_view_details_button.clicked.connect(self.on_profile_view_details_button_clicked)
        self.edit_button.clicked.connect(self.on_edit_button_clicked)
        self.edit_button_2.clicked.connect(self.on_edit_button_clicked)

        # REVISE: move to separate function later
        # resize table cols to header/content
        self.application_table.resizeColumnsToContents()
        self.application_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.selected_stat_table.resizeColumnsToContents()
        self.selected_stat_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.archive_table.resizeColumnsToContents()
        self.archive_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

    #### Navbar Button Functions
    def on_navbar_account_button_clicked(self):
        self.current_tab.setCurrentIndex(0)
        
    def on_navbar_notif_button_clicked(self):
        self.current_tab.setCurrentIndex(1)
        
    def on_navbar_home_button_clicked(self):
        self.current_tab.setCurrentIndex(2)
        
        bar_width = self.mon_label.width()
        
        # set bar sizes here
        # NOTE: Need to convert the height (second arg) to %, min is 0 max is 100
        # So the height needs to be a variable that passes the % of task done per day
        self.mon_bar.setMinimumSize(bar_width, 10)
        self.tue_bar.setMinimumSize(bar_width, 30)
        self.wed_bar.setMinimumSize(bar_width, 100)
        self.thu_bar.setMinimumSize(bar_width, 40)
        self.fri_bar.setMinimumSize(bar_width, 70)
        self.sat_bar.setMinimumSize(bar_width, 40)
        self.sun_bar.setMinimumSize(bar_width, 30)
        
        # adjust radial bar
        # code block to adjust radial bar
        # NOTE: put this in a function and then just edit it to make it easy to adjust the radial bar later on
        test = """
        #monthly_radialbar {
            border-radius: 45px;
            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{start_stop} rgba(247, 182, 0, 255), stop:{end_stop} rgba(255, 255, 255, 0));
        }
        """
        
        value = 60 # Change this to adjust the radial bar
        converted_value = value / 100.0 
        start_stop = str(converted_value - 0.001)
        end_stop = str(converted_value)
        
        test = test.replace("{start_stop}", start_stop).replace("{end_stop}", end_stop)
        
        self.monthly_radialbar.setStyleSheet(test)
    
    def on_navbar_application_button_clicked(self):
        self.current_tab.setCurrentIndex(3)
    
    def on_navbar_archive_button_clicked(self):
        self.current_tab.setCurrentIndex(4)
    
    # NOTE: Need to pass selected applicant from table
    # NOTE: Need DB to be finished/established before I can continue this
    def on_applicant_selected_clicked(self):
        self.current_tab.setCurrentIndex(5)
        self.application_form_header_label.setText("Test")
    
    # NOTE: Need to pass current applicant selected from Applicant Profile
    # NOTE: Need DB to be finished/established before I can continue this    
    def on_profile_view_details_button_clicked(self):
        self.current_tab.setCurrentIndex(6)
        self.application_form_header_label.setText("Test")
    
    # NOTE: Need to pass current applicant selected from Applicant Profile
    # NOTE: Need DB to be finished/established before I can continue this    
    def on_edit_button_clicked(self):
        self.current_tab.setCurrentIndex(7)
        self.application_form_header_label.setText("Edit Application")
        
        # insert code to populate saved data here
        
    def on_new_application_button_clicked(self):
        self.current_tab.setCurrentIndex(7)
        self.application_form_header_label.setText("New Application")

    def on_navbar_logout_button_clicked(self):
        # insert logout here
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())