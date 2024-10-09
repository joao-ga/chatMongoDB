from Database.entities import User, Message
from Database.mongohandler import Operation

if __name__ == '__main__':
    operation = Operation()

    email_input = input("Enter your email: ")
    password_input = input("Enter your password: ")

    if operation.find_user(email_input, password_input):
        print("Login feito!")
        nickname_from = 'Joao'
        #pegar o nome da pessoa na consulta

        nickname_to = input("Destinatário: ")
        message_content = input("Menssagem: ")

        encrypted_content = Message.encrypt_message(password_input, message_content)
        message = Message(nickname_from, nickname_to, encrypted_content)

        message_id = operation.add_new_message(message)
        print("Menssagem enviada!")

        #fazer condição de ler mensagem, apenas se o usuario clicar no botao ler mensagens
        decrypted_message = Message.decrypt_message(password_input, encrypted_content)
        print(f"Decrypted message: {decrypted_message}")
    else:
        print("Login failed! Invalid credentials.")
