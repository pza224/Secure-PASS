from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import json

class AESManager:
    def __init__(self, key: bytes):
        self.key = key

    def encrypt(self, data: str) -> str:
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))

        # Combine the IV, ciphertext, and tag into one dictionary for storage
        encrypted_data = {
            "nonce": base64.b64encode(cipher.nonce).decode('utf-8'),
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
            "tag": base64.b64encode(tag).decode('utf-8')
        }

        # Return the data as a JSON string
        return json.dumps(encrypted_data)

    def decrypt(self, encrypted_data: str) -> str:
        try:
            # Decode the encrypted data from JSON
            data = json.loads(encrypted_data)
            
            nonce = base64.b64decode(data["nonce"])
            ciphertext = base64.b64decode(data["ciphertext"])
            tag = base64.b64decode(data["tag"])

            cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

            return decrypted_data.decode('utf-8')

        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")
