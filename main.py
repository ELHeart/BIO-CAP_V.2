from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog,
    QHBoxLayout, QFormLayout, QMenuBar, QAction, QSplashScreen
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import (Qt, QTimer)
from oauth2client.service_account import ServiceAccountCredentials
from classes import (SignUpDialog, BioDataApp, ConnectionErrorDialog, ConfirmDialog, LoginDialog, SplashScreen)
from functions import (resource_path, is_internet_available, init_google_sheets_api, add_user, find_user,
                       encrypt_password, check_password)
import gspread, socket, bcrypt, sys, os, json, requests


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon(resource_path('cc.ico')))

    splash_image_path = resource_path('cc.png')  # Use resource_path for the image
    splash_image = QPixmap(splash_image_path)
    splash = SplashScreen(splash_image, 3000)  # 3000 milliseconds = 3 seconds
    splash.show_splash_screen()
    app.processEvents()  # Ensure the splash screen is displayed properly

    # Check for internet connection
    if not is_internet_available():
        connection_dialog = ConnectionErrorDialog()
        if connection_dialog.exec_() == QDialog.Rejected:
            sys.exit()  # Exit the application if there is no internet connection after retrying

    # Shows the sign-up dialog first
    signup = SignUpDialog()
    result = signup.exec_()

    # If the user closes the sign-up dialog or clicks "Sign In", show the login dialog
    if result == QDialog.Rejected:
        login = LoginDialog()
        if login.exec_() == QDialog.Accepted:
            ex = BioDataApp()
            ex.show()
            app.exec_()
    else:
        login = LoginDialog()
        if login.exec_() == QDialog.Accepted:
            ex = BioDataApp()
            ex.show()
            app.exec_()
