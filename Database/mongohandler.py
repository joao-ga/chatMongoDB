import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
from pymongo import MongoClient
from Database.entities import Message
from Database.utils import derive_key_from_password


class Operation:
    def __init__(self):
        self.connection_string = "mongodb+srv://jbiazonferreira:123456qwerty@aulas.joxwh.mongodb.net/?retryWrites=true&w=majority&appName=aulas"
        self.client = MongoClient(self.connection_string)
        self.db = self.client["chatMongo"]
        self.users_collection = self.db.Users
        self.messages_collection = self.db.messages

    def send_message_to_db(self, sender, recipient, message, password):
        salt = os.urandom(16)
        key = derive_key_from_password(password, salt)
        encrypted_message = Message.encrypt_message(message, key)

        message_document = {
            'from': sender,
            'to': recipient,
            'message': encrypted_message,
            'salt': urlsafe_b64encode(salt).decode('utf-8')
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
            show_message = input("Você gostaria de ver a mensagem? (sim/não): ").strip().lower()

            if show_message == 'sim':
                print(f"Mensagem criptografada: {msg['message']}")

                salt = urlsafe_b64decode(msg['salt'])
                key = derive_key_from_password(password, salt)

                decrypted_message = Message.decrypt_message(msg['message'], key)
                print(f"Mensagem descriptografada: {decrypted_message}")

        if not messages_found:
            print("Nenhuma nova mensagem recebida.")

        send_new_message = input("Você gostaria de enviar uma nova mensagem? (sim/não): ").strip().lower()
        return send_new_message == 'sim'

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
