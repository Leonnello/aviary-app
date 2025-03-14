import sqlite3
from PyQt6.QtWidgets import QMessageBox

class Database:
    def __init__(self, db_name="app_database.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS application (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                applicant_name TEXT NOT NULL UNIQUE,
                first_name TEXT NOT NULL,
                middle_name TEXT,
                last_name TEXT NOT NULL,
                gender TEXT CHECK (gender IN ('Male', 'Female', 'Other')) NOT NULL,
                birthday DATE NOT NULL,
                country_of_citizenship TEXT NOT NULL,
                contact_num TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                passport_num TEXT DEFAULT 'Empty',
                passport_expiry DATE,
                travel_history TEXT DEFAULT 'Empty',
                travel_purpose TEXT DEFAULT 'Empty',
                visa_type TEXT,
                refile BOOLEAN DEFAULT 0,
                educ_background TEXT CHECK (educ_background IN ('Empty', 
                                                                'Associate', 
                                                                'Bachelor', 
                                                                'Doctorate', 
                                                                'High School', 
                                                                'Master', 
                                                                'None', 
                                                                'Other')),
                employment_stat BOOLEAN DEFAULT 0,
                job_title TEXT DEFAULT 'Empty',
                job_train_req BOOLEAN DEFAULT 0,
                econ_sector TEXT CHECK (econ_sector IN ('Empty',
                                                        'Advanced Manufacturing',
                                                        'Aerospace', 
                                                        'Agribusiness', 
                                                        'Automotive', 
                                                        'Biotechnology', 
                                                        'Construction', 
                                                        'Educational Services', 
                                                        'Energy', 
                                                        'Finance', 
                                                        'Geospatial', 
                                                        'Health Care', 
                                                        'Homeland Security', 
                                                        'Hospitality', 
                                                        'IT', 
                                                        'Other Economic Sector', 
                                                        'Retail', 
                                                        'Transportation')),
                wage INT,
                wage_unit TEXT CHECK (wage_unit IN ('Empty', 'Hourly', 'Daily', 'Biweekly', 'Weekly', 'Monthly', 'Yearly')),
                case_status TEXT CHECK (case_status IN ('Pending', 'Awaiting Result', 'Approved', 'Denied', 'Withdrawn')) DEFAULT 'Pending',
                is_archived BOOLEAN NOT NULL DEFAULT 0,
                recc TEXT,
                processed_date DATE,
                submitted_date DATE,
                missing_doc TEXT,
                for_doc_replacement TEXT,
                missing_data TEXT      
            )
        ''')
        self.conn.commit()

    def register_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    def validate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone() is not None  # Returns True if user exists
    
    def create_application(self, **data):
        try:
            columns = ", ".join([f'"{column}"' for column in data.keys()])
            values = tuple(data.values())
            
            self.cursor.execute(f"INSERT INTO application ({columns}) VALUES ({', '.join(['?'] * len(values))})", values)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as Error:
            QMessageBox.warning(None, "Application Creation Failed", str(Error))
            return False
    
    def edit_application(self, id, **data):
        try:
            set_clause = ", ".join([f'"{column}" = ?' for column in data.keys()])
            values = tuple(data.values()) + (id,)
            
            self.cursor.execute("SELECT * FROM application WHERE id = ?", (id,))

            self.cursor.execute(f"UPDATE application SET {set_clause} WHERE id = ?", values)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as Error:
            QMessageBox.warning(None, "Application Edit Failed", str(Error))
            return False
        
    def display_application(self, id):
        try:
            self.cursor.execute(f"SELECT * FROM application WHERE id = ?", (id,))
            applicant = self.cursor.fetchone()
            
            return applicant
        except sqlite3.DatabaseError as Error:
            return None
        
    def display_database(self, table : str):
        try:
            self.cursor.execute(f"SELECT * FROM {table}")
            
            rows = self.cursor.fetchall()
            cols = [desc[0] for desc in self.cursor.description]
            return cols, rows
        except sqlite3.DatabaseError as Error:
            return None
    
    def query_case_status(self, table : str, case_status : str):
        try:
            self.cursor.execute(f"SELECT * FROM {table} WHERE case_status = ?", (case_status,))
            
            rows = self.cursor.fetchall()
            
            cols = [desc[0] for desc in self.cursor.description]
            return cols, rows
        except sqlite3.DatabaseError as Error:
            return None

    def close(self):
        self.conn.close()
