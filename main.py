from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog,
    QHBoxLayout, QStackedWidget, QMainWindow, QFileDialog, QFormLayout, QMenuBar, QAction, QSplashScreen
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import (Qt, QTimer, pyqtSignal)
from oauth2client.service_account import ServiceAccountCredentials
from classes import (SignUpWidget, BioDataApp, ConnectionErrorDialog, ConfirmDialog, LoginWidget, MainWindow,
                     SplashScreen)
from functions import (resource_path, is_internet_available, init_google_sheets_api, add_user, find_user,
                       encrypt_password, check_password)
import gspread, socket, bcrypt, sys, os, json, requests


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon(resource_path('cc.ico')))

    splash_image_path = resource_path('cc.png')
    splash_image = QPixmap(splash_image_path)
    splash = SplashScreen(splash_image, 3000)  # 3000 milliseconds = 3 seconds
    splash.show_splash_screen()
    app.processEvents()  # Ensure the splash screen is displayed properly

    # Check for internet connection
    if not is_internet_available():
        connection_dialog = ConnectionErrorDialog()
        if connection_dialog.exec_() == QDialog.Rejected:
            sys.exit()  # Exit the application if there is no internet connection after retrying

    # Show the welcome window
    Main_window = MainWindow()
    Main_window.show()

    # Create the BioDataApp instance but do not show it yet
    bio_data_app = BioDataApp()

    # Connect the login_successful signal to the show method of the BioDataApp instance
    Main_window.login_widget.login_successful.connect(bio_data_app.show)
    # Also connect the login_successful signal to the close_window method of the WelcomeWindow
    Main_window.login_widget.login_successful.connect(Main_window.close_window)

    sys.exit(app.exec_())
