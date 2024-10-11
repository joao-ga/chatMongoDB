from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.fernet import InvalidToken
from cryptography.fernet import Fernet

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
        return {
            "nickname_from": self.nickname_from,
            "nickname_to": self.nickname_to,
            "content": self.content
        }

    @staticmethod
    def encrypt_message(message, key):
        fernet = Fernet(key)
        encrypted_message = fernet.encrypt(message.encode())
        return urlsafe_b64encode(encrypted_message).decode('utf-8')

    @staticmethod
    def decrypt_message(encrypted_message, key):
        fernet = Fernet(key)
        encrypted_message = urlsafe_b64decode(encrypted_message.encode('utf-8'))
        decrypted_message = fernet.decrypt(encrypted_message).decode()
        return decrypted_message
