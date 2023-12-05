from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog,
    QHBoxLayout, QFormLayout, QMenuBar, QFileDialog, QAction, QSplashScreen
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import (Qt, QTimer)
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import gspread, socket, bcrypt, sys, os

# Function to determine the resource path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def is_internet_available(host="8.8.8.8", port=53, timeout=3):
    """
    Check if there is an internet connection available to a specified host.
    The default host is Google's primary DNS server.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


# Function to initialize the Google Sheets connection
def init_google_sheets_api(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_path = resource_path('bio-cap-c9841b6b39e2.json')  # Use resource_path for the JSON file
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet, creds


# Function to hash a password
def encrypt_password(password):  # Reduced work factor
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


# Function to check a hashed password
def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)


# Function to find a user login data in the Google Sheet
def find_user(username, user_password):
    sheet, creds = init_google_sheets_api('Credentials')
    if sheet is None:
        return False
    users = sheet.get_all_records()
    for user in users:
        if user['Username'] == username:
            stored_password = user['PasswordHash'].encode('utf-8')
            if check_password(stored_password, user_password):
                return True
    return False


# Function to add a new user login data to the Google Sheet
def add_user(username, hashed_password):
    sheet, creds = init_google_sheets_api('Credentials')
    if sheet is not None:
        # Decode the hashed password to a UTF-8 string before appending
        sheet.append_row([username, hashed_password.decode('utf-8')])
