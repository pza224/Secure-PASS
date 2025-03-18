Secure-PASS 🛡️🔐

A secure password manager built with PyQt for the GUI and AES encryption for security.
Features

    Securely store and manage passwords 🔑
    AES encryption for password protection 🛡️
    Built-in password generator 🔢
    Dark mode UI 🌙
    Master password setup on first launch

Installation Instructions
1. Clone the Repository

git clone https://github.com/pza224/Secure-PASS.git
cd Secure-PASS

2. Install Dependencies

Ensure you have Python 3.9+ installed, then run:

pip install -r requirements.txt

3. Run the Application

To launch the password manager, run:

python -m src.gui.gui

Usage

    First Launch: You will be prompted to create a master password. This password is required every time you open the app.
    Adding a Password: Enter the service name, username, website, and password, then click "Add Password".
    Retrieving Passwords: Select a saved service to view its details.
    Deleting a Password: Select a service and press "Delete".
    Generating a Password: Use the built-in password generator for strong passwords.

Troubleshooting

    White Splash Screen? Ensure splash_image.png is inside src/gui/
    Dependencies Not Found? Run pip install -r requirements.txt
    Issues with Git? Try git pull origin main --rebase before pushing updates
