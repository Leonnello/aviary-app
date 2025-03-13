from PyQt6.QtWidgets import QWidget, QInputDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

import requests
import random
import webbrowser
import os
import threading
from flask import Flask, request, redirect, jsonify


load_dotenv()

FIREBASE_DB_URL = "https://aviaryfirebase-23384-default-rtdb.firebaseio.com"
FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

GOOGLE_AUTH_URL = (
    f"https://accounts.google.com/o/oauth2/auth"
    f"?client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope=email profile"
    f"&response_type=code"
    "&access_type=offline"
    "&prompt=consent"
)

app = Flask(__name__)

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self = uic.loadUi("QtGUI/login.ui", self)
        self.login_button.clicked.connect(self.on_login)
        self.noacc_link.mousePressEvent = self.on_noacc_link_clicked
        self.already_link.mousePressEvent = self.on_already_link_clicked
        self.forgot_link.mousePressEvent = self.on_forgot_link_clicked
        self.register_button.clicked.connect(self.on_register_clicked)
        self.change_send_button.clicked.connect(self.on_change_send_clicked)
        #self.change_login_button.clicked.connect(self.on_change_login_clicked)
        self.google_login_button.clicked.connect(self.login_with_google)

        self.register_send_button.clicked.connect(self.send_verification_email)
        self.change_back_button.clicked.connect(lambda: self.currentPage.setCurrentIndex(0))

        self.user_id_token = None

    def login_with_google(self):
        self.flask_thread = threading.Thread(target=app.run, kwargs={"port": 5000}, daemon=True)
        self.flask_thread.start()
        webbrowser.open(GOOGLE_AUTH_URL)
        self.check_google_login()

    def check_google_login(self):
        #check if the Flask server stored the login token.
        if os.path.exists("google_login_success.txt"):
            with open("google_login_success.txt", "r") as f:
                self.user_id_token = f.read().strip()
            os.remove("google_login_success.txt")

            QMessageBox.information(self, "Success", "Google login successful!")
            self.open_main_window()
            return

        #keep checking every 1 second
        QTimer.singleShot(1000, self.check_google_login)

    def on_login(self):
        email = self.login_username.text().strip()
        password = self.login_password.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Email and password cannot be empty!")
            return

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if "idToken" in data:
            self.user_id_token = data["idToken"]
            QMessageBox.information(self, "Success", "Login successful!")
            self.open_main_window()
        else:
            error_msg = data.get("error", {}).get("message", "Login failed!")
            QMessageBox.warning(self, "Error", error_msg)

    def open_main_window(self):
        from app import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def on_noacc_link_clicked(self, event):
        self.currentPage.setCurrentIndex(1)

    def on_already_link_clicked(self, event):
        self.currentPage.setCurrentIndex(0)

    def on_forgot_link_clicked(self, event):
        email = self.login_username.text().strip()  # Assuming this is where the email is entered

        if not email:
            QMessageBox.warning(self, "Error", "Email cannot be empty!")
            return

        dummy_password = "dummypassword123"

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        payload = {
            "email": email,
            "password": dummy_password,
            "returnSecureToken": True
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if "idToken" in data:
            self.user_id_token = data["idToken"]

        if "error" in data:
            error_msg = data["error"].get("message", "")

            if "EMAIL_NOT_FOUND" in error_msg:
                QMessageBox.warning(self, "Error", "This email is not registered.")

            else:
                QMessageBox.information(self, "Success", "Email is registered. Proceeding to change password.")
                self.currentPage.setCurrentIndex(2) #go to Change password1
                self.register_email.setText(email)

    def on_register_clicked(self, event):
        email = self.register_email.text().strip()
        password = self.register_password.text().strip()
        entered_code = self.register_verification.text().strip()

        if not email or not password or not entered_code:
            QMessageBox.warning(self, "Error", "All fields must be filled!")
            return

        #fetch stored verification code
        db_url =  f"{FIREBASE_DB_URL}/verification_codes/{email.replace('.', ',')}.json"

        response = requests.get(db_url)
        stored_code = response.json()

        print(f"Entered Code: {entered_code}, Stored Code: {stored_code}")

        if stored_code is None:
            QMessageBox.warning(self, "Error", "No verification code found for this email!")
            return

        if entered_code.strip() != str(stored_code).strip():
            QMessageBox.warning(self, "Error", "Invalid verification code!")
            return

        #register user in Firebase Auth
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=payload)
        data = response.json()

        if "idToken" in data:
            QMessageBox.information(self, "Success", "Registration successful!")
            self.currentPage.setCurrentIndex(0)  #goto login page
        else:
            error_msg = data.get("error", {}).get("message", "Registration failed!")
            QMessageBox.warning(self, "Error", error_msg)

    def send_verification_email(self):
            email = self.register_email.text().strip()

            if not email:
                QMessageBox.warning(self, "Error", "Email cannot be empty!")
                return

            verification_code = str(random.randint(100000, 999999))  #generate a 6-digit code

            #send Email via SendGrid
            message = Mail(
                from_email=SENDER_EMAIL,
                to_emails=email,
                subject="Your Verification Code",
                plain_text_content=f"Your verification code is: {verification_code}"
            )

            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                sg.send(message)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to send email: {e}")
                return

            #Store the verification code in Firebase
            formatted_email = email.replace('.', ',')
            db_url = f"{FIREBASE_DB_URL}/verification_codes/{formatted_email}.json"
            response = requests.put(db_url, json=verification_code)

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Verification code sent to your email.")
            else:
                QMessageBox.warning(self, "Error", "Failed to store verification code in Firebase!")


    def on_change_send_clicked(self, event):
        email = self.lineEdit_4.text().strip()

        if not email:
            QMessageBox.warning(self, "Error", "Email cannot be empty!")
            return

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}"
        payload = {
            "requestType": "PASSWORD_RESET",
            "email": email
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if "email" in data:
            QMessageBox.information(self, "Success", "A password reset email has been sent.")
            self.currentPage.setCurrentIndex(0) #goto login page
        else:
            error_msg = data.get("error", {}).get("message", "Failed to send reset email!")
            QMessageBox.warning(self, "Error", error_msg)

################################"""Google login server stuff"""################################
@app.route("/callback")
def google_callback():
    """Handles OAuth2 response from Google."""
    auth_code = request.args.get("code")
    if not auth_code:
        return jsonify({"error": "Authorization code not received"}), 400

    # Exchange auth code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=payload)
    data = response.json()

    if "id_token" in data:
        id_token = data["id_token"]

        #sign in to Firebase with the ID token
        firebase_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={FIREBASE_API_KEY}"
        firebase_payload = {
            "postBody": f"id_token={id_token}&providerId=google.com",
            "requestUri": REDIRECT_URI,
            "returnIdpCredential": True,
            "returnSecureToken": True,
        }

        firebase_response = requests.post(firebase_url, json=firebase_payload)
        firebase_data = firebase_response.json()

        if "idToken" in firebase_data:
            with open("google_login_success.txt", "w") as f:
                f.write(firebase_data["idToken"])  #store token for pyqt to read
            return "Login successful! You can close this window."
        else:
            return "Firebase authentication failed."

    return jsonify(data)

def shutdown_flask():
    """Stop Flask server after login"""
    requests.get("http://127.0.0.1:5000/shutdown")

@app.route("/shutdown")
def shutdown():
    """Shutdown Flask server"""
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        func()
    return "Server shutting down..."
