import unittest
from src.encryption.aes import AESManager

class TestAESManager(unittest.TestCase):
    def setUp(self):
        self.key = b'secretkey1234567'  # 16-byte key for AES
        self.aes_manager = AESManager(self.key)

    def test_encryption_decryption(self):
        data = "password123"
        encrypted_data = self.aes_manager.encrypt(data)
        decrypted_data = self.aes_manager.decrypt(encrypted_data)
        self.assertEqual(data, decrypted_data)

if __name__ == '__main__':
    unittest.main()
