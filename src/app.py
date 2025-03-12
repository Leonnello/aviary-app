from PyQt6.QtWidgets import QApplication, QWidget, QHeaderView, QMessageBox
from database import Database 

from PyQt6 import uic

import sys
import custom_gui_classes as custom


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self = uic.loadUi("QtGUI/login.ui", self)
        self.db = Database ()
        
        self.login_button.clicked.connect(self.on_login)
        self.noacc_link.mousePressEvent = self.on_noacc_link_clicked
        self.already_link.mousePressEvent = self.on_already_link_clicked
        self.forgot_link.mousePressEvent = self.on_forgot_link_clicked
        self.register_button.clicked.connect(self.on_register_clicked)
        self.change_submit_button.clicked.connect(self.on_change_submit_clicked)
        self.change_login_button.clicked.connect(self.on_change_login_clicked)

        

    def on_login(self):
        username = self.login_username.text()
        password = self.login_password.text()
        
        if self.db.validate_user(username, password):
            QMessageBox.information(self, "Login Success", "Welcome, " + username)
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
            

        # self.main_window = MainWindow()
        # self.main_window.show()
        # self.close()

    def on_noacc_link_clicked(self, event):
        self.currentPage.setCurrentIndex(1)

    def on_already_link_clicked(self, event):
        self.currentPage.setCurrentIndex(0)

    def on_forgot_link_clicked(self, event):
        self.currentPage.setCurrentIndex(2)

    def on_register_clicked(self, event):
        email = self.register_email.text()
        password = self.register_password.text()

        if self.db.register_user(email, password):
            QMessageBox.information(self, "Registration Success", "Account created! Please log in.")
        else:
            QMessageBox.warning(self, "Registration Failed", "Username already taken.")
        
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
        
    def on_change_submit_clicked(self, event):
        # NOTE: change passord

        self.currentPage.setCurrentIndex(3)

    def on_change_login_clicked(self, event):
        # NOTE: register new password then login

        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self = uic.loadUi("QtGUI/form.ui", self)
        self.db = Database()
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

        # NOTE REVISE: move to separate function later
        # resize table cols to header/content
        self.application_table.resizeColumnsToContents()
        self.application_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.selected_stat_table.resizeColumnsToContents()
        self.selected_stat_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.archive_table.resizeColumnsToContents()
        self.archive_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        # Drag n Drog for File Upload
        upload_area = custom.UploadFrame(self.docs_body_container)
        upload_area.fileDropped.connect(self.on_new_file_uploaded)
        
        ### interactable QFrame
        # Homepage
        # Current Status
        new_app = custom.InteractableFrame(self.curr_stat_new_applications_container)
        pending_app = custom.InteractableFrame(self.curr_stat_pending_container)
        awaiting_app = custom.InteractableFrame(self.curr_stat_awaiting_response_container)
        approved_app = custom.InteractableFrame(self.curr_stat_approved_container)
        denied_app = custom.InteractableFrame(self.curr_stat_denied_container)
        # Task bar graphs
        mon_bar = custom.InteractableFrame(self.mon_bar, "#219EBC")
        tue_bar = custom.InteractableFrame(self.tue_bar, "#219EBC")
        wed_bar = custom.InteractableFrame(self.wed_bar, "#219EBC")
        thu_bar = custom.InteractableFrame(self.thu_bar, "#219EBC")
        fri_bar = custom.InteractableFrame(self.fri_bar, "#219EBC")
        sat_bar = custom.InteractableFrame(self.sat_bar, "#219EBC")
        sun_bar = custom.InteractableFrame(self.sun_bar, "#219EBC")
        # Applicant Report page
        past_approved = custom.InteractableFrame(self.past_approved, "#81E1BB") 
        past_denied = custom.InteractableFrame(self.past_denied, "#E18181") 
        missing_docs = custom.InteractableFrame(self.missing_docs, "#E18181") 
        
        # connect interactableframe to leftClicked signal
        new_app.leftClicked.connect(self.on_new_application_button_clicked)
        pending_app.leftClicked.connect(lambda: self.display_table(self.selected_stat_table, "pending_app"))
        awaiting_app.leftClicked.connect(lambda: self.display_table(self.selected_stat_table, "awaiting_app"))
        approved_app.leftClicked.connect(lambda: self.display_table(self.selected_stat_table, "approved_app"))
        denied_app.leftClicked.connect(lambda: self.display_table(self.selected_stat_table, "denied_app"))
            
            
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

    def on_navbar_logout_button_clicked(self):
        # insert logout here

        self.login_page = LoginPage()
        self.login_page.show()
        self.close()
    
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
        
        # NOTE: insert code to populate saved data here
        
    def on_new_application_button_clicked(self):
        self.current_tab.setCurrentIndex(7)
        self.application_form_header_label.setText("New Application")

    #### Interactable Frame Clicked Functions
    

    #### QTable Manipulation Functions
    def display_table(self, table_widget, db_name):
        print(table_widget, db_name)
        
        # NOTE: insert code to handle the ff
        # get db columns as QTableWidget headers
        # get rows from db and display to QTableWidget
        
        if db_name == "pending_app":
            # NOTE: Filter Case Status == Pending on db
            # display results to QTableWidget
            # COLUMNS: Applicant Name, Missing Document, For Document Replacement, Mising Data
            
            self.selected_stat_label.setText("Pending")
            pass
        elif db_name == "awaiting_app":
            # COLUMNS: Applicant Name, Visa Type, Submitted at
            
            self.selected_stat_label.setText("Awaiting")
            pass
        elif db_name == "approved_app":
            # COLUMNS: Applicant Name, Visa Type, Processed at
            
            self.selected_stat_label.setText("Approved")
            pass
        elif db_name == "denied_app":
            # COLUMNS: Applicant Name, Visa Type, Processed at, Recommendation Text
            
            self.selected_stat_label.setText("Denied")
            pass
        
        
        pass
    
    

    #### File Upload
    def on_new_file_uploaded(self, file_name):
        new_file_interactable = custom.FileObjectFrame(file_name, self.docs_file_container)
        
        self.docs_file_container.layout().setSpacing(10)
        self.docs_file_container.layout().addWidget(new_file_interactable)
        
    #### General helper functions
    # format tablewidget row to dict
    def format_data(self, table_widget, selected_row):
        formatted_data = {}
        
        # get text for each cell in a row
        for col in range(table_widget.columnCount()):
            data = table_widget.item(selected_row, col)
            formatted_data[table_widget.horizontalHeaderItem(col).text()] = data.text()
        
        return formatted_data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    login_page.currentPage.setCurrentIndex(0);
    sys.exit(app.exec())
