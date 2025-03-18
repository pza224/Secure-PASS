import unittest
from unittest.mock import patch, mock_open
from src.storage.storage import StorageManager

class TestStorageManager(unittest.TestCase):

    def setUp(self):
        """Setup code that runs before every test"""
        self.filename = 'passwords.json'
        self.storage_manager = StorageManager(self.filename)

    @patch("builtins.open", new_callable=mock_open, read_data='{"service1": "encrypted_pass1"}')
    def test_load_passwords(self, mock_file):
        """Test that the load_password function reads data from the file correctly"""
        print("Before loading passwords")  # Debugging output
        passwords = self.storage_manager.load_passwords()
        print("After loading passwords")  # Debugging output
        
        # Assert that open was called with the correct parameters
        mock_file.assert_called_with(self.filename, 'r')
        self.assertEqual(passwords, {"service1": "encrypted_pass1"})

    @patch("builtins.open", new_callable=mock_open)
    def test_save_passwords(self, mock_file):
        """Test that the save_password function writes data to the file correctly"""
        passwords = {"service1": "encrypted_pass1"}

        self.storage_manager.save_password(passwords)

        # Assert the file was opened with 'w' mode for writing
        mock_file.assert_called_with(self.filename, 'w')

        # Get the handle for the mocked file
        handle = mock_file()

        # Correctly concatenate the arguments passed to 'write'
        written_data = ''.join(call[0][0] for call in handle.write.call_args_list)

        # Assert that the full data is written as expected
        self.assertEqual(written_data, '{"service1": "encrypted_pass1"}')

if __name__ == '__main__':
    unittest.main()
