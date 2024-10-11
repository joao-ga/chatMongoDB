import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
from dns.dnssecalgs import cryptography
from pymongo import MongoClient
from Database.entities import Message
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet



class Operation:
    def __init__(self):
        self.connection_string = "mongodb+srv://jbiazonferreira:123456qwerty@aulas.joxwh.mongodb.net/?retryWrites=true&w=majority&appName=aulas"
        self.client = MongoClient(self.connection_string)
        self.db = self.client["chatMongo"]
        self.users_collection = self.db.Users
        self.messages_collection = self.db.messages

    def derive_key_from_password(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return urlsafe_b64encode(kdf.derive(password.encode()))

    def decrypt(self, encrypted_message, key):
        fernet = Fernet(key)
        decrypted_message = fernet.decrypt(encrypted_message).decode()
        return decrypted_message

    def send_message_to_db(self, sender, recipient, message, password):
        salt = os.urandom(16)
        key = self.derive_key_from_password(password, salt)
        encrypted_message = Message.encrypt_message(message, key)
        salt64 = urlsafe_b64encode(salt).decode('utf-8')
        print(salt64, ' salt64')
        print(encrypted_message, ' encrypted_message')

        message_document = {
            'from': sender,
            'to': recipient,
            'message': encrypted_message,
            'salt': salt64
        }
        self.messages_collection.insert_one(message_document)
        print(f"Mensagem de {sender} para {recipient} enviada e criptografada com sucesso!")
        print("--------------------------------------------------------------------------------")

    def check_received_messages(self, user_email, password):
        messages = self.messages_collection.find({'to': user_email})
        messages_found = False

        for msg in messages:
            messages_found = True
            print(f"Você tem uma mensagem de {msg['from']}.")

            show_message = input("Você gostaria de ver a mensagem? (s/n): ").strip().lower()
            if show_message == 's':
                salt = urlsafe_b64decode(msg['salt'])
                key = self.derive_key_from_password(password, salt)

                try:
                    decrypted_message = Message.decrypt_message(msg['message'], key)
                    print(f"Mensagem descriptografada: {decrypted_message}")
                except Exception as e:
                    print(f"Erro: {str(e)}")  # Mostra o erro detalhado
                    print("A mensagem não pôde ser descriptografada. Chave incorreta ou mensagem alterada.")

        if not messages_found:
            print("Nenhuma nova mensagem recebida.")

        send_new_message = input("Você gostaria de enviar uma nova mensagem? (s/n): ").strip().lower()
        return send_new_message == 's'

    def login(self):
        while True:
            email = input("Digite seu e-mail: ")
            password = input("Digite sua senha: ")
            user = self.users_collection.find_one({'email': email, 'password': password})

            if user:
                print("Login bem-sucedido!")
                return email, password
            else:
                print("E-mail ou senha incorretos. Tente novamente.")
