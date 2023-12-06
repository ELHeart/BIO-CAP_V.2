from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog,
    QHBoxLayout, QFormLayout, QMenuBar, QFileDialog, QAction, QSplashScreen
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import (Qt, QTimer)
from oauth2client.service_account import ServiceAccountCredentials
from functions import (resource_path, is_internet_available, init_google_sheets_api, add_user, find_user,
                       encrypt_password, check_password)
import gspread, socket, bcrypt, sys, os, json, requests


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
        self.uploaded_image_link = None
        self.age = QLineEdit()
        self.lastName = QLineEdit()
        self.middleName = QLineEdit()
        self.firstName = QLineEdit()
        # Inside the BioDataApp class

        self.pictureLabel = QLabel("No picture selected.")
        self.pictureButton = QPushButton("Upload Picture")
        self.pictureButton.clicked.connect(self.upload_picture)

        self.init_ui()
        self.sheet, self.creds = init_google_sheets_api('Bio-Data')
        # Now self.creds can be used to access Google Drive API

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
        # Inside the init_ui method of the BioDataApp class
        form_layout.addRow("Picture:", self.pictureLabel)
        form_layout.addRow("", self.pictureButton)

        # Submit button
        submitButton = QPushButton("Submit")
        submitButton.clicked.connect(self.confirm_dialog)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(submitButton, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)

    # Function to get the access token from Google OAuth 2.0
    def get_access_token(self):
        scope = ['https://www.googleapis.com/auth/drive.file']
        creds_path = resource_path('bio-cap-c9841b6b39e2.json')  # Use resource_path for the JSON file
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        access_token_info = creds.get_access_token()
        return access_token_info.access_token

    def upload_image_to_drive(self, file_path):
        try:
            access_token = self.get_access_token()  # Assuming you have a method to get the access token
            headers = {
                "Authorization": "Bearer " + access_token
            }
            metadata = {
                "name": os.path.basename(file_path),
                # If you have a folder ID stored as an instance attribute
                "parents": [self.folder_id] if hasattr(self, 'folder_id') else []
            }
            # Use a context manager to ensure the file is open during the upload
            with open(file_path, "rb") as file:
                files = {
                    'data': ('metadata', json.dumps(metadata), 'application/json; charset=UTF-8'),
                    'file': ('file', file)
                }
                r = requests.post(
                    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                    headers=headers,
                    files=files
                )
            r.raise_for_status()
            file_id = r.json()['id']

            # Set the file to be publicly accessible
            permission = {
                'type': 'anyone',
                'role': 'reader',
            }
            r = requests.post(
                f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions",
                headers=headers,
                data=json.dumps(permission)
            )
            r.raise_for_status()

            # Return the web view link
            file_link = f"https://drive.google.com/uc?id={file_id}"
            return file_link
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    # Inside the BioDataApp class
    def upload_picture(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Picture", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            # Upload the image and get the shareable link
            # noinspection PyArgumentList
            file_link = self.upload_image_to_drive(file_name)
            # Set the file link to the label to display it (or store it in an instance variable)
            self.pictureLabel.setText(file_link)
            # Load the image and set it as a thumbnail
            pixmap = QPixmap(file_name)
            self.pictureLabel.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            # Store the file link in an instance variable for later use
            self.uploaded_image_link = file_link

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
        # Include the image link in the data to be submitted
        image_link = self.uploaded_image_link

        # Write data to Google Sheets
        self.sheet.append_row([first_name, middle_name, last_name, age, image_link])

        # Show a SUCCESS message box when data is submitted
        QMessageBox.information(self, "Success", "Data submitted successfully!")

        # Clear the form fields for a new entry
        self.firstName.clear()
        self.middleName.clear()
        self.lastName.clear()
        self.age.clear()
        # Clear the image link
        self.uploaded_image_link = None
        self.pictureLabel.setText("No picture selected.")
