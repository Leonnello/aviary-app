from PyQt6.QtWidgets import QApplication, QWidget, QHeaderView, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt, QDate
from PyQt6 import uic

from database import Database 
from datetime import datetime

import sys
import custom_gui_classes as custom

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self = uic.loadUi("QtGUI/form.ui", self)
        self.db = Database()
        
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
        self.submit_button.clicked.connect(self.on_form_submit_button_clicked)
        self.change_stat_button.clicked.connect(self.on_change_stat_button_clicked)
        self.application_table.cellDoubleClicked.connect(lambda row, col: self.on_applicant_selected_clicked(row, col, self.application_table))
        self.archive_table.cellDoubleClicked.connect(lambda row, col: self.on_applicant_selected_clicked(row, col, self.archive_table))
        self.selected_stat_table.cellDoubleClicked.connect(lambda row, col: self.on_applicant_selected_clicked(row, col, self.selected_stat_table))
        
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
        # prevent multiple function calls
        if self.current_tab.currentIndex() == 2:
            return
        
        self.current_tab.setCurrentIndex(2)
        
        self.display_table(self.selected_stat_table, "pending_app")
        
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
        # prevent multiple function calls
        if self.current_tab.currentIndex() == 3:
            return
        
        self.current_tab.setCurrentIndex(3)

        self.display_table(self.application_table, "application")
        
    def on_navbar_archive_button_clicked(self):
        self.current_tab.setCurrentIndex(4)
        
        self.archive_table.resizeColumnsToContents()
        self.archive_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

    def on_navbar_logout_button_clicked(self):
        # insert logout here
        from login_page import LoginPage

        #issue: somehow 3 login instances show up after logging out
        if hasattr(self, "login_page") and self.login_page is not None:
            self.login_page.close()  #Ensure previous instance is closed

        self.login_page = LoginPage()
        self.login_page.show()
        self.login_page.currentPage.setCurrentIndex(0)
        self.close()
    
    def on_applicant_selected_clicked(self, row, col, table_widget):
        # prevent multiple function calls
        if self.current_tab.currentIndex() == 5:
            return
        
        self.current_tab.setCurrentIndex(5)
        print("row: ", row)
        self.applicant_id = table_widget.verticalHeaderItem(row).text()
        
        # populate profile with available data from db
        # ugly code :(
        data = self.db.display_application(self.applicant_id)
        
        self.applicant_profile_header_label.setText(data[1])

        birthday = datetime.strptime(data[6], "%Y-%m-%d")
        self.profile_age_data.setText(str( datetime.today().year - birthday.year - 
                                          ((datetime.today().month, datetime.today().day) < (birthday.month, birthday.day))))
        self.profile_gender_data.setText(data[5])
        self.profile_citizenship_data.setText(data[7])
        self.profile_passport_num_data.setText(str(data[10]))
        self.profile_passport_expiry_data.setText(data[11])
        self.profile_visa_type_data.setText(data[14])
        self.profile_destination_data.setText("USA")
        self.profile_purpose_data.setText(data[13])
        
        if data[15] == 0:
            self.profile_refile_data.setText("No")
        else:
            self.profile_refile_data.setText("Yes")
            
        if data[17] == 0:
            self.profile_employment_status_data.setText("Unemployed")
        else:
            self.profile_employment_status_data.setText("Employed")
    
    # NOTE: Needs result from AI model
    def on_profile_view_details_button_clicked(self):
        # prevent multiple function calls
        if self.current_tab.currentIndex() == 6:
            return
        
        self.current_tab.setCurrentIndex(6)
        self.msg_box_open = False
        
        # populate profile with available data from db
        # ugly code :(
        data = self.db.display_application(self.applicant_id)
        
        self.applicant_report_header_label.setText(data[1])
        
        birthday = datetime.strptime(data[6], "%Y-%m-%d")
        self.profile_age_data_2.setText(str( datetime.today().year - birthday.year - 
                                          ((datetime.today().month, datetime.today().day) < (birthday.month, birthday.day))))
        self.profile_gender_data_2.setText(data[5])
        self.profile_citizenship_data_2.setText(data[7])
        self.profile_passport_num_data_2.setText(str(data[10]))
        self.profile_passport_expiry_data_2.setText(data[11])
        self.profile_visa_type_data_2.setText(data[14])
        self.profile_destination_data_2.setText("USA")
        self.profile_purpose_data_2.setText(data[13])
        
        if data[15] == 0:
            self.profile_refile_data_2.setText("No")
        else:
            self.profile_refile_data_2.setText("Yes")
            
        if data[17] == 0:
            self.profile_employment_status_data_2.setText("Unemployed")
        else:
            self.profile_employment_status_data_2.setText("Employed")
            
        # NOTE: Insert results from AI here
       
    def on_edit_button_clicked(self):
        # prevent multiple function calls
        if self.current_tab.currentIndex() == 7:
            return
        
        self.current_tab.setCurrentIndex(7)
        
        data = self.db.display_application(self.applicant_id)
        
        self.application_form_header_label.setText(f"Edit Application for {data[1]}")

        # populate saved data 
        # more ugly code :(
        self.first_name_edit.setText(data[2])
        self.middle_name_edit.setText(data[3])
        self.last_name_edit.setText(data[4])
        
        self.birthday_selector.setDate(QDate.fromString(data[6], "yyyy-MM-dd"))
        self.passport_expiry_selector.setDate(QDate.fromString(data[11], "yyyy-MM-dd"))
        
                    
        print(data[6])
        print(data[11])
        
        self.contact_number_edit.setText(data[8])
        self.email_edit.setText(data[9])
        self.passport_number_edit.setText(data[10])
        self.travel_history_edit.setText(data[12])
        self.travel_purpose_edit.setText(data[13])
        self.job_title_edit.setText(data[18])
        self.wage_edit.setText(str(data[21]))
        
        self.gender_combobox.setCurrentIndex(self.gender_combobox.findText(data[5]))
        self.citizenship_combobox.setCurrentIndex(self.citizenship_combobox.findText(data[7]))

        if data[14] == 'Empty':
            self.visa_type_combobox.setCurrentIndex(0)
        else:
            self.visa_type_combobox.setCurrentIndex(self.visa_type_combobox.findText(data[14]))
        
        if data[15] == 0:
            self.refile_combobox.setCurrentIndex(2)
        else:
            self.refile_combobox.setCurrentIndex(1)
        
        if data[16] == 'Empty':
            self.educ_background_combobox.setCurrentIndex(0)
        else:
            self.educ_background_combobox.setCurrentIndex(self.educ_background_combobox.findText(data[16]))
        
        if data[17] == 0:
            self.employment_status_combobox.setCurrentIndex(2)
        else:
            self.employment_status_combobox.setCurrentIndex(1)
        
        if data[19] == 0:
            self.job_training_req_combobox.setCurrentIndex(2)
        else:
            self.job_training_req_combobox.setCurrentIndex(1)
            
        if data[20] == 'Empty':
            self.economic_sect_combobox.setCurrentIndex(0)
        else:
            self.economic_sect_combobox.setCurrentIndex(self.economic_sect_combobox.findText(data[20]))
        
        if data[22] == 'Empty':
            self.wage_type_combobox.setCurrentIndex(0)
        else:
            self.wage_type_combobox.setCurrentIndex(self.wage_type_combobox.findText(data[22]))
        
    def on_new_application_button_clicked(self):
        self.current_tab.setCurrentIndex(7)
        self.application_form_header_label.setText("New Application")
        
        # set default date value to an invalid date
        self.birthday_selector.setDate(self.birthday_selector.minimumDate())
        self.passport_expiry_selector.setDate(self.passport_expiry_selector.minimumDate())
        
        # reset form values
        self.first_name_edit.setText("")
        self.middle_name_edit.setText("")
        self.last_name_edit.setText("")
        self.contact_number_edit.setText("")
        self.email_edit.setText("")
        self.passport_number_edit.setText("")
        self.travel_history_edit.setText("")
        self.travel_purpose_edit.setText("")
        self.job_title_edit.setText("")
        self.wage_edit.setText("")
        
        self.gender_combobox.setCurrentIndex(0)
        self.citizenship_combobox.setCurrentIndex(0)
        self.visa_type_combobox.setCurrentIndex(0)
        self.refile_combobox.setCurrentIndex(0)
        self.educ_background_combobox.setCurrentIndex(0)
        self.employment_status_combobox.setCurrentIndex(0)
        self.job_training_req_combobox.setCurrentIndex(0)
        self.economic_sect_combobox.setCurrentIndex(0)
        self.wage_type_combobox.setCurrentIndex(0)
        
    def on_form_submit_button_clicked(self):
        # get data from form inputs, 
        # i hate this but it is, what it is :(
        data_container = {}
        data_container["gender"] = self.gender_combobox.currentText()
        data_container["birthday"] = self.birthday_selector.date().toString("yyyy-MM-dd")
        data_container["country_of_citizenship"] = self.citizenship_combobox.currentText()
        data_container["contact_num"] = self.contact_number_edit.text()
        data_container["email"] = self.email_edit.text()
        data_container["passport_num"] = self.passport_number_edit.text()
        data_container["passport_expiry"] = self.passport_expiry_selector.date().toString("yyyy-MM-dd")
        data_container["travel_history"] = self.travel_history_edit.text()
        data_container["travel_purpose"] = self.travel_purpose_edit.text()
        data_container["job_title"] = self.job_title_edit.text()
        data_container["wage"] = self.wage_edit.text()
        
        # req fields
        missing_req = []
        
        req_fields = {
            "First Name" : self.first_name_edit,
            "Last Name" : self.last_name_edit,
            "Contact Number" : self.contact_number_edit,
            "Email Address" : self.email_edit,
        }
        req_combobox = {
            "Country of Citizenship" : self.citizenship_combobox,
            "Gender" : self.gender_combobox
        }    
        
        for key, field in req_fields.items():
            if field.text().strip() == "":
                missing_req.append(key)
        
        for key, field in req_combobox.items():
            if field.currentIndex() == 0:
                missing_req.append(key)
                
        if self.birthday_selector.date() == self.birthday_selector.minimumDate():
            missing_req.append("Birthday")
                
        # validate req fields, return error if missing fields
        if missing_req:
            QMessageBox.warning(self, "Application Creation Failed", f"Please fill out required fields:\n" + "\n".join(missing_req))
            return
        
        # combine names for easy display, but save others incase ig
        data_container["applicant_name"] = " ".join(filter(None, [self.first_name_edit.text(), self.middle_name_edit.text(), self.last_name_edit.text()]))
        data_container["first_name"] = self.first_name_edit.text()
        data_container["middle_name"] = self.middle_name_edit.text()
        data_container["last_name"] = self.last_name_edit.text()
        
        # combobox default vals processing
        if self.visa_type_combobox.currentIndex() == 0:
            data_container["visa_type"] = 'Empty'
        else:
            data_container["visa_type"] = self.visa_type_combobox.currentText()
            
        if self.educ_background_combobox.currentIndex() == 0:
            data_container["educ_background"] = 'Empty'
        else:
            data_container["educ_background"] = self.educ_background_combobox.currentText()
            
        if self.wage_type_combobox.currentIndex() == 0:
            data_container["wage_unit"] = 'Empty'
        else:
            data_container["wage_unit"] = self.wage_type_combobox.currentText()
            
        if self.economic_sect_combobox.currentIndex() == 0:
            data_container["econ_sector"] = 'Empty'
        else:
            data_container["econ_sector"] = self.economic_sect_combobox.currentText()
            
        if self.refile_combobox.currentText() == 'Yes':
            data_container["visa_type"] = 1
            
        if self.employment_status_combobox.currentText() == 'Employed':
            data_container["employment_stat"] = 1
            
        if self.job_training_req_combobox.currentText() == 'Yes':
            data_container["job_train_req"] = 1
        
        # create new row on db
        if self.application_form_header_label.text() == "New Application":
            if self.db.create_application(**data_container):
                QMessageBox.information(None, "Application Creation Success", "New Application has been successfully created.")
                self.on_navbar_application_button_clicked()
        # edit row
        else:
            if self.db.edit_application(self.applicant_id, **data_container):
                QMessageBox.information(None, "Application Edit Success", "Application has been successfully edited.")
                # self.on_applicant_selected_clicked(int(self.applicant_id)-1, None , )
                self.on_navbar_application_button_clicked()
        
    def on_change_stat_button_clicked(self):
        # prevent multiple function calls
        if self.msg_box_open:
            return
    
        self.msg_box_open = True
        
        # QMessageBox gui for change case prompt
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Change Case Status")
        msg_box.setText(f"Change status for Row ID: {self.applicant_id}")
        
        selected_status = ""
        
        approved_button = msg_box.addButton("Approved", QMessageBox.ButtonRole.AcceptRole)
        denied_button = msg_box.addButton("Denied", QMessageBox.ButtonRole.RejectRole)
        withdrawn_button = msg_box.addButton("Withdrawn", QMessageBox.ButtonRole.AcceptRole)
        
        msg_box.exec()

        # Get the selected value
        if msg_box.clickedButton() == approved_button:
            selected_status = "Approved"
        elif msg_box.clickedButton() == denied_button:
            selected_status = "Denied"
        elif msg_box.clickedButton() == withdrawn_button:
            selected_status = "Withdrawn"
        else:
            return
        
        data = {"case_status" : selected_status}
        if selected_status == "Withdrawn":
            data["is_archived"] = 1
        
        self.db.edit_application(self.applicant_id, **data)
        
        self.on_navbar_application_button_clicked()
   
    #### Interactable Frame Clicked Functions
    

    #### QTable Manipulation Functions
    def display_table(self, table_widget, db_name):
        # clear table_widget so there's no leftover data
        table_widget.setRowCount(0)
        
        if db_name == "pending_app":
            # COLUMNS: Applicant Name, Missing Document, For Document Replacement, Mising Data
            
            self.selected_stat_label.setText("Pending")
            cols, data = self.db.query_case_status("application", "Pending")
            
            if data:
                selected_cols = [cols.index(col) for col in ["applicant_name", "missing_doc", "for_doc_replacement", "missing_data"] if col in cols]
            
                table_widget.setRowCount(len(data))
                table_widget.setColumnCount(len(selected_cols))
                table_widget.setHorizontalHeaderLabels(["Applicant Name", "Missing Document", "For Document Replacement", "Missing Data"])
                
                row_id = []
                
                for row_index, row in enumerate(data):
                    row_id.append(str(row[cols.index("id")]))
                    for col_index, actual_col in enumerate(selected_cols):
                        item = QTableWidgetItem(str(row[actual_col]))
                        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                        table_widget.setItem(row_index, col_index, item)
                
                table_widget.setVerticalHeaderLabels(row_id)
        elif db_name == "awaiting_app":
            # COLUMNS: Applicant Name, Visa Type, Submitted at
            
            self.selected_stat_label.setText("Awaiting Result")
            cols, data = self.db.query_case_status("application", "Awaiting Result")

            if data:
                selected_cols = [cols.index(col) for col in ["applicant_name", "visa_type", "submitted_date"] if col in cols]
            
                table_widget.setRowCount(len(data))
                table_widget.setColumnCount(len(selected_cols))
                table_widget.setHorizontalHeaderLabels(["Applicant Name", "Visa Type", "Submitted at"])
                
                row_id = []
                
                for row_index, row in enumerate(data):
                    row_id.append(str(row[cols.index("id")]))
                    for col_index, actual_col in enumerate(selected_cols):
                        item = QTableWidgetItem(str(row[actual_col]))
                        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                        table_widget.setItem(row_index, col_index, item)

                table_widget.setVerticalHeaderLabels(row_id)
        elif db_name == "approved_app":
            # COLUMNS: Applicant Name, Visa Type, Processed at
            
            self.selected_stat_label.setText("Approved")
            cols, data = self.db.query_case_status("application", "Approved")
            
            if data:
                selected_cols = [cols.index(col) for col in ["applicant_name", "visa_type", "processed_date"] if col in cols]
                table_widget.setRowCount(len(data))
                table_widget.setColumnCount(len(selected_cols))
                table_widget.setHorizontalHeaderLabels(["Applicant Name", "Visa Type", "Processed at"])
                
                row_id = []
                
                for row_index, row in enumerate(data):
                    row_id.append(str(row[cols.index("id")]))
                    for col_index, actual_col in enumerate(selected_cols):
                        item = QTableWidgetItem(str(row[actual_col]))
                        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                        table_widget.setItem(row_index, col_index, item)
                        
                table_widget.setVerticalHeaderLabels(row_id)
        elif db_name == "denied_app":
            # COLUMNS: Applicant Name, Visa Type, Processed at, Recommendation Text
            
            self.selected_stat_label.setText("Denied")
            cols, data = self.db.query_case_status("application", "Denied")
            

            if data:
                selected_cols = [cols.index(col) for col in ["applicant_name", "visa_type", "processed_date", "recc"] if col in cols]
            
                table_widget.setRowCount(len(data))
                table_widget.setColumnCount(len(selected_cols))
                table_widget.setHorizontalHeaderLabels(["Applicant Name", "Visa Type", "Processed at", "Recommendation Text"])
                
                row_id = []
                
                for row_index, row in enumerate(data):
                    row_id.append(str(row[cols.index("id")]))
                    for col_index, actual_col in enumerate(selected_cols):
                        item = QTableWidgetItem(str(row[actual_col]))
                        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                        table_widget.setItem(row_index, col_index, item)

                table_widget.setVerticalHeaderLabels(row_id)
        elif db_name == "application":
            # COLUMNS: Applicant Name, Case Status, Visa Type, Email Address, Contact Number

            cols, data = self.db.display_database(db_name)
            
            if data:
                selected_cols = [cols.index(col) for col in ["applicant_name", "case_status", "visa_type", "email", "contact_num"] if col in cols]
            
                table_widget.setRowCount(len(data))
                table_widget.setColumnCount(len(selected_cols))
                # table_widget.setHorizontalHeaderLabels(["Applicant Name", "Case Status", "Visa Type", "Email Address", "Contact Number"])
                
                row_id = []
                
                for row_index, row in enumerate(data):
                    row_id.append(str(row[cols.index("id")]))
                    for col_index, actual_col in enumerate(selected_cols):
                        item = QTableWidgetItem(str(row[actual_col]))
                        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                        table_widget.setItem(row_index, col_index, item)

                table_widget.setVerticalHeaderLabels(row_id)
        
        table_widget.resizeColumnsToContents()
        table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

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
    from login_page import LoginPage
    app = QApplication(sys.argv)
    login_page = LoginPage()
    # login_page = MainWindow() # NOTE: Temp for testing
    login_page.show()
    login_page.currentPage.setCurrentIndex(0);
    # login_page.current_tab.setCurrentIndex(0); # NOTE: Temp for testing
    sys.exit(app.exec())
