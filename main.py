from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog,
    QHBoxLayout, QStackedWidget, QMainWindow, QFileDialog, QFormLayout, QMenuBar, QAction, QSplashScreen, QFrame
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import (Qt, QTimer, pyqtSignal)
from oauth2client.service_account import ServiceAccountCredentials
from classes import (SignUpWidget, BioDataApp, ConnectionErrorDialog, ConfirmDialog, LoginWidget, MainWindow,
                     SplashScreen)
from functions import (resource_path, is_internet_available, init_google_sheets_api, add_user, find_user,
                       encrypt_password, check_password, stylesheet)
import gspread
import socket
import bcrypt
import sys
import os
import json
import requests


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon(resource_path('BIOCAP.ico')))
    app.setStyleSheet(stylesheet)

    splash_image_path = resource_path('ICON.jpg')
    splash_image = QPixmap(splash_image_path)
    splash = SplashScreen(splash_image, 100)  # 1000 milliseconds = 1 second
    splash.show_splash_screen()
    app.processEvents()  # Ensure the splash screen is displayed properly

    # Check for internet connection
    if not is_internet_available():
        connection_dialog = ConnectionErrorDialog()
        if connection_dialog.exec_() == QDialog.Rejected:
            sys.exit()  # Exit the application if there is no internet connection after retrying

    # Show the welcome window
    Main_window = MainWindow()

    # Create the BioDataApp instance but do not show it yet
    bio_data_app = BioDataApp()

    # Connect the login_successful signal to the show method of the BioDataApp instance
    Main_window.login_widget.login_successful.connect(bio_data_app.show)
    # Also connect the login_successful signal to the close_window method of the WelcomeWindow
    Main_window.login_widget.login_successful.connect(Main_window.close_window)
    # Connect the finished signal of the splash screen to the function that shows the main window
    splash.finished.connect(Main_window.show)

    sys.exit(app.exec_())
