import aes_pkcs5
from pymongo import MongoClient
import hashlib

class User:
    def __init__(self, nickname: str, email: str, password: str):
        self.nickname = nickname
        self.email = email
        self.password = password


class Message:
    def __init__(self, nickname_from: str, nickname_to: str, content: str):
        self.nickname_to = nickname_to
        self.content = content
        self.nickname_from = nickname_from

    def to_dict(self):
        """Returns a dictionary of the message."""
        return {
            "nickname_from": self.nickname_from,
            "nickname_to": self.nickname_to,
            "content": self.content
        }

    @staticmethod
    def encrypt_message(key: str, message: str) -> str:

        key_bytes = hashlib.sha256(key.encode()).digest()
        encrypted_message = aes_pkcs5.encrypt(message.encode('utf-8'))
        return encrypted_message.hex()

    @staticmethod
    def decrypt_message(key: str, encrypted_message: str) -> str:

        key_bytes = hashlib.sha256(key.encode()).digest()
        encrypted_bytes = bytes.fromhex(encrypted_message)
        decrypted_message = aes_pkcs5.decrypt(key_bytes, encrypted_bytes)
        return decrypted_message.decode('utf-8')



