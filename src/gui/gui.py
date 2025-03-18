from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget
from src.encryption.aes import AESManager
from src.storage.storage import StorageManager
from src.password_generator import generate_password  # ✅ Re-added this import
import sys
import os

class PasswordManagerGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SecurePass Password Manager")
        self.setGeometry(100, 100, 500, 400)

        self.setDarkTheme()  # Apply dark mode
        self.storage_manager = StorageManager("passwords.json")
        self.aes_manager = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.initUI()

    def initUI(self):
        """Shows the splash screen before transitioning to the master password input."""
        self.splash_label = QLabel(self)
        
        # Load and set the splash image
        splash_path = os.path.abspath("src/gui/splash_image.png")  # Ensure correct path
        pixmap = QtGui.QPixmap(splash_path)
        
        if pixmap.isNull():
            print("Error: Splash image not found at", splash_path)  # Debugging info
            self.splash_label.setText("SecurePass Loading...")  # Fallback text
        else:
            self.splash_label.setPixmap(pixmap.scaled(500, 400, QtCore.Qt.KeepAspectRatio))

        self.layout.addWidget(self.splash_label)

        self.repaint()  # Force UI update
        QtWidgets.QApplication.processEvents()

        # Wait 5 seconds, then transition
        QtCore.QTimer.singleShot(5000, self.showMasterPasswordScreen)

    def showMasterPasswordScreen(self):
        """Displays the master password input after the splash screen."""
        self.clearLayout()

        self.master_label = QLabel("Enter Master Password:")
        self.master_input = QLineEdit()
        self.master_input.setEchoMode(QLineEdit.Password)
        self.master_button = QPushButton("Unlock")
        self.error_label = QLabel("")  # Error message placeholder

        self.layout.addWidget(self.master_label)
        self.layout.addWidget(self.master_input)
        self.layout.addWidget(self.master_button)
        self.layout.addWidget(self.error_label)

        self.master_button.clicked.connect(self.unlock)

        # Check if master password exists
        storage_data = self.storage_manager.load_storage()
        if storage_data.get("master_password") is None:
            self.master_label.setText("Set a Master Password:")
            self.master_button.setText("Set Password")

    def unlock(self):
        """Handles unlocking the password manager."""
        master_password = self.master_input.text()
        storage_data = self.storage_manager.load_storage()

        if storage_data.get("master_password") is None:
            # First-time setup: store the new master password
            self.storage_manager.set_master_password(master_password)
            self.error_label.setText("Master password set! Please log in again.")
            return

        if not self.storage_manager.check_master_password(master_password):
            self.error_label.setText("Invalid password. Try again.")
            return

        key = master_password.encode("utf-8").ljust(32, b'\0')
        self.aes_manager = AESManager(key)
        self.showMainMenu()

    def showMainMenu(self):
        """Displays the main password manager UI."""
        self.clearLayout()

        self.service_input = QLineEdit()
        self.service_input.setPlaceholderText("Service Name")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("Website URL")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # ✅ Generate Password Button
        self.generate_button = QPushButton("Generate Password")
        self.generate_button.clicked.connect(self.generate_password)

        self.add_button = QPushButton("Add Password")
        self.list_widget = QListWidget()
        self.delete_button = QPushButton("Delete Selected")
        self.message_label = QLabel("")

        self.layout.addWidget(QLabel("Add New Password:"))
        self.layout.addWidget(self.service_input)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.website_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.generate_button)  # ✅ Added button here
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(QLabel("Saved Passwords:"))
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.message_label)

        self.add_button.clicked.connect(self.add_password)
        self.list_widget.itemClicked.connect(self.get_password)
        self.delete_button.clicked.connect(self.delete_password)

        self.load_passwords()

    def generate_password(self):
        """Generates a 50-character secure password and sets it in the password field."""
        new_password = generate_password(50)
        self.password_input.setText(new_password)
        self.message_label.setText("Generated secure password!")

    def add_password(self):
        """Saves a new password."""
        service = self.service_input.text()
        username = self.username_input.text()
        website = self.website_input.text()
        password = self.password_input.text()

        if not (service and username and website and password):
            self.message_label.setText("All fields are required!")
            return

        encrypted_password = self.aes_manager.encrypt(password)
        self.storage_manager.save_password(service, {
            "username": username,
            "website": website,
            "password": encrypted_password
        })

        self.list_widget.addItem(service)
        self.message_label.setText(f"Password for {service} added successfully!")
        self.clear_inputs()

    def get_password(self, item):
        """Displays saved password details."""
        service = item.text()
        passwords = self.storage_manager.load_passwords()

        if service in passwords:
            data = passwords[service]
            decrypted_password = self.aes_manager.decrypt(data["password"])
            self.message_label.setText(f"{service} - Username: {data['username']}, Password: {decrypted_password}")

    def delete_password(self):
        """Deletes the selected password."""
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            return

        service = selected_item.text()
        passwords = self.storage_manager.load_passwords()

        if service in passwords:
            del passwords[service]
            self.storage_manager.save_storage({"master_password": self.storage_manager.load_storage()["master_password"], "passwords": passwords})
            self.list_widget.takeItem(self.list_widget.row(selected_item))
            self.message_label.setText(f"Password for {service} deleted.")

    def load_passwords(self):
        """Loads stored passwords into the list."""
        self.list_widget.clear()
        passwords = self.storage_manager.load_passwords()
        for service in passwords:
            self.list_widget.addItem(service)

    def clear_inputs(self):
        """Clears input fields."""
        self.service_input.clear()
        self.username_input.clear()
        self.website_input.clear()
        self.password_input.clear()

    def clearLayout(self):
        """Removes all widgets from the layout."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def setDarkTheme(self):
        """Applies a dark mode theme."""
        dark_theme = """
        QWidget {
            background-color: #2B2B2B;
            color: #FFFFFF;
            font-size: 14px;
        }
        QLineEdit {
            background-color: #3C3F41;
            color: white;
            border: 1px solid #555;
            padding: 5px;
        }
        QPushButton {
            background-color: #505050;
            color: white;
            border: 1px solid #777;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #606060;
        }
        QLabel {
            color: white;
        }
        """
        self.setStyleSheet(dark_theme)

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = PasswordManagerGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
