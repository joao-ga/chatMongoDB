from Database.mongohandler import Operation
from Database.utils import derive_key_from_password  # Use o caminho correto para utils

def chat(operation, user_email, password):
    recipient = input("Digite o e-mail do destinatário: ")
    message = input("Digite a mensagem: ")
    operation.send_message_to_db(user_email, recipient, message, password)

if __name__ == '__main__':
    operation = Operation()

    # Realiza o login do usuário
    email, password = operation.login()

    # Inicia o chat
    chat(operation, email, password)
