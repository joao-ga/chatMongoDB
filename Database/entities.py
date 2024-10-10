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
        return encrypted_message

    @staticmethod
    def decrypt_message(encrypted_message, key):
        fernet = Fernet(key)
        decrypted_message = fernet.decrypt(encrypted_message).decode()
        return decrypted_message
