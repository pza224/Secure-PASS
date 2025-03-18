import json
import os
from Crypto.Hash import SHA256

class StorageManager:
    def __init__(self, filename="passwords.json"):
        self.filename = filename
        self._initialize_storage()

    def _initialize_storage(self):
        """Ensures storage file exists and contains required keys."""
        if not os.path.exists(self.filename):
            self.save_storage({"master_password": None, "passwords": {}})
        else:
            # Check if the file is valid JSON and contains required keys
            try:
                data = self.load_storage()
                if "master_password" not in data or "passwords" not in data:
                    self.save_storage({"master_password": None, "passwords": {}})
            except json.JSONDecodeError:
                # Reset the file if it is corrupted
                self.save_storage({"master_password": None, "passwords": {}})

    def set_master_password(self, master_password):
        """Hashes and stores the master password."""
        hashed_password = SHA256.new(master_password.encode()).hexdigest()
        data = self.load_storage()
        data["master_password"] = hashed_password
        self.save_storage(data)

    def check_master_password(self, master_password):
        """Verifies the master password against stored hash."""
        data = self.load_storage()
        hashed_input = SHA256.new(master_password.encode()).hexdigest()
        return hashed_input == data["master_password"]

    def save_password(self, service, data):
        """Saves an encrypted password to storage."""
        storage_data = self.load_storage()
        if "passwords" not in storage_data:
            storage_data["passwords"] = {}  # Ensure passwords key exists
        storage_data["passwords"][service] = data
        self.save_storage(storage_data)

    def load_passwords(self):
        """Loads all stored passwords."""
        return self.load_storage().get("passwords", {})

    def load_storage(self):
        """Loads the storage JSON file."""
        with open(self.filename, "r") as file:
            return json.load(file)

    def save_storage(self, data):
        """Saves data to the storage JSON file."""
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

