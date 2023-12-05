from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog,
    QHBoxLayout, QFormLayout, QMenuBar, QAction, QSplashScreen
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import (Qt, QTimer)
from oauth2client.service_account import ServiceAccountCredentials
import gspread, socket, bcrypt, sys, os

from functions import (resource_path, is_internet_available, init_google_sheets_api, add_user, find_user,
                       encrypt_password, check_password)


# SplashScreen class
class SplashScreen(QSplashScreen):
    def __init__(self, pixmap, timeout):
        super().__init__(pixmap)
        self.timeout = timeout

    def show_splash_screen(self):
        self.show()
        QTimer.singleShot(self.timeout, self.close)


class ConnectionErrorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Connection Error')
        self.setWindowIcon(QIcon(resource_path('cc.ico')))  # Use resource_path for the icon
        self.setModal(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("No internet connection. Please check your network settings."))

        # Retry button
        retry_button = QPushButton("Retry")
        retry_button.clicked.connect(self.retry_connection)
        layout.addWidget(retry_button)

        self.setLayout(layout)

    def retry_connection(self):
        if is_internet_available():
            self.accept()  # Close the dialog if the internet is available
        else:
            QMessageBox.warning(self, "Connection Error", "Still no internet connection. Please check your "
                                                          "network settings again.")


# SignUpDialog class creates a sign-up dialog box
class SignUpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sign Up')
        # Set the window icon
        self.setStyleSheet(
            "QDialog { background-color: #f2f2f2; } QPushButton { background-color: #4CAF50; color: white; } "
            "QLineEdit { padding: 5px; } QLabel { font-weight: bold; }")
        self.setModal(True)

        layout = QVBoxLayout()

        # Username and password entry points.
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)

        # Sign up button creation
        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(self.register_user)
        layout.addWidget(signup_button)

        # Button to switch to the Sign In window
        signin_button = QPushButton("Sign In")
        signin_button.clicked.connect(self.switch_to_signin)
        layout.addWidget(signin_button)

        self.setLayout(layout)

    def init_ui(self):
        self.setWindowTitle('Sign Up')
        # Set the window icon
        self.setModal(True)

        form_layout = QFormLayout()

        # Username and password entry points.
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Username:", self.username)
        form_layout.addRow("Password:", self.password)

        # Sign up and Sign in buttons
        buttons_layout = QHBoxLayout()
        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(self.register_user)
        buttons_layout.addWidget(signup_button)

        signin_button = QPushButton("Sign In")
        signin_button.clicked.connect(self.switch_to_signin)
        buttons_layout.addWidget(signin_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def switch_to_signin(self):
        self.done(0)  # Close the sign-up dialog with a rejection code 0

    def register_user(self):
        username = self.username.text()
        password = self.password.text()
        hashed_password = encrypt_password(password)  # Use bcrypt to hash the password

        # Add user to Google Sheets
        add_user(username, hashed_password)

        # Successful data entry alert
        QMessageBox.information(self, "Success", "You have signed up successfully!")
        self.accept()


# Login Dialog Class
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        # Set the window icon
        self.setStyleSheet(
            "QDialog { background-color: #f2f2f2; } QPushButton { background-color: #4CAF50; color: white; } "
            "QLineEdit { padding: 5px; } QLabel { font-weight: bold; }")
        self.setModal(True)

        layout = QVBoxLayout()

        # Login Data entry
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)

        # Login Button creation and credentials check
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.check_credentials)
        layout.addWidget(login_button)

        self.setLayout(layout)

    # Function checks login data from allows rentry
    def check_credentials(self):
        username = self.username.text()
        password = self.password.text()

        # Check credentials against Google Sheets
        if find_user(username, password):
            self.accept()  # Closes the dialog box and continues
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password. Please try again.")
            self.username.clear()
            self.password.clear()


# ConfirmDialog Class
class ConfirmDialog(QDialog):
    def __init__(self, parent, first_name, middle_name, last_name, age):
        super().__init__(parent)
        self.setWindowTitle('Confirm Data')
        self.setWindowIcon(QIcon(resource_path('cc.ico')))  # Use resource_path for the icon
        # Set the window icon

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"First Name: {first_name}"))
        layout.addWidget(QLabel(f"Middle Name: {middle_name}"))
        layout.addWidget(QLabel(f"Last Name: {last_name}"))
        layout.addWidget(QLabel(f"Age: {age}"))

        # Confirm Button creation
        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.accept)
        button_layout.addWidget(self.confirm_button)

        # Edit Button creation
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.reject)
        button_layout.addWidget(self.edit_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)


# BioDataApp Class
class BioDataApp(QWidget):
    def __init__(self):
        super().__init__()
        self.age = QLineEdit()
        self.lastName = QLineEdit()
        self.middleName = QLineEdit()
        self.firstName = QLineEdit()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Bio-Data Collection Application')  # Set the window title
        # Set the window icon
        self.setStyleSheet("QWidget { background-color: #f2f2f2; } QPushButton { background-color: #4CAF50; color:"
                           " white; } QLineEdit { padding: 5px; } QLabel { font-weight: bold; }")  # Stylesheet for the
        # window

        form_layout = QFormLayout()

        # Data Entry fields
        self.firstName.setPlaceholderText("Enter first name")
        self.middleName.setPlaceholderText("Enter middle name (Skip if none)")
        self.lastName.setPlaceholderText("Enter last name")
        self.age.setPlaceholderText("Enter age")

        form_layout.addRow("First Name:", self.firstName)
        form_layout.addRow("Middle Name (Skip if none):", self.middleName)
        form_layout.addRow("Last Name:", self.lastName)
        form_layout.addRow("Age:", self.age)

        # Submit button
        submitButton = QPushButton("Submit")
        submitButton.clicked.connect(self.confirm_dialog)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(submitButton, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)

    # Function checks data type for age entry and brings up data confirmation dialog box
    def confirm_dialog(self):
        # Checks if age input is an integer
        try:
            age = int(self.age.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Invalid input for age. Please enter an integer.")
            return

        dialog = ConfirmDialog(self, self.firstName.text(), self.middleName.text(), self.lastName.text(), age)
        if dialog.exec_():
            self.submit_data()

    # Function writes data to Google Sheets
    def submit_data(self):
        age = int(self.age.text())
        first_name = self.firstName.text()
        middle_name = self.middleName.text()
        last_name = self.lastName.text()

        # Write data to Google Sheets
        sheet = init_google_sheets_api('Bio-Data')
        sheet.append_row([first_name, middle_name, last_name, age])

        # Show a SUCCESS message box when data is submitted
        QMessageBox.information(self, "Success", "Data submitted successfully!")

        # Clear the form fields for a new entry
        self.firstName.clear()
        self.middleName.clear()
        self.lastName.clear()
        self.age.clear()
