import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from src.encryption.aes import AESManager
from src.storage.storage import StorageManager

class PasswordManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.correct_master_password = "XTDG2025#^"  # Permanent master password
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SecurePass Password Manager")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Enter Master Password:")
        layout.addWidget(self.label)
        
        self.master_password_input = QLineEdit()
        self.master_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.master_password_input)
        
        self.submit_button = QPushButton("Login")
        self.submit_button.clicked.connect(self.check_master_password)
        layout.addWidget(self.submit_button)
        
        self.setLayout(layout)

    def check_master_password(self):
        master_password = self.master_password_input.text()
        if master_password == self.correct_master_password:
            self.start_password_manager(master_password)
        else:
            QMessageBox.warning(self, "Error", "Invalid master password. Try again.")

    def start_password_manager(self, master_password):
        self.key = master_password.encode("utf-8").ljust(32, b'\0')
        self.storage_manager = StorageManager("passwords.json")
        self.aes_manager = AESManager(self.key)
        
        self.manager_window = QWidget()
        self.manager_window.setWindowTitle("Password Manager")
        self.manager_window.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout()
        
        self.service_input = QLineEdit()
        self.service_input.setPlaceholderText("Service Name")
        layout.addWidget(self.service_input)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("Website URL")
        layout.addWidget(self.website_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        layout.addWidget(self.password_input)
        
        self.add_button = QPushButton("Add Password")
        self.add_button.clicked.connect(self.add_password)
        layout.addWidget(self.add_button)
        
        self.list_button = QPushButton("List Passwords")
        self.list_button.clicked.connect(self.list_passwords)
        layout.addWidget(self.list_button)
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)
        
        self.manager_window.setLayout(layout)
        self.manager_window.show()
        self.close()
    
    def add_password(self):
        service = self.service_input.text()
        username = self.username_input.text()
        website = self.website_input.text()
        password = self.password_input.text()
        
        if service and username and website and password:
            encrypted_password = self.aes_manager.encrypt(password)
            self.storage_manager.save_password({
                service: {
                    "username": username,
                    "website": website,
                    "password": encrypted_password
                }
            })
            QMessageBox.information(self, "Success", f"Password for {service} added successfully.")
        else:
            QMessageBox.warning(self, "Error", "All fields must be filled.")
    
    def list_passwords(self):
        passwords = self.storage_manager.load_passwords()
        if passwords:
            output_text = "Stored Passwords:\n"
            for service, data in passwords.items():
                try:
                    decrypted_password = self.aes_manager.decrypt(data["password"])
                    output_text += f"{service}:\n    Username: {data['username']}\n    Website: {data['website']}\n    Password: {decrypted_password}\n\n"
                except Exception as e:
                    output_text += f"{service}: Failed to decrypt password ({str(e)})\n"
            self.output_area.setText(output_text)
        else:
            self.output_area.setText("No passwords stored.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManagerApp()
    window.show()
    sys.exit(app.exec_())
