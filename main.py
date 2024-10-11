from Database.mongohandler import Operation



#integrantes do grupo
# Erico Conte Tezoto - 23004160
# Caio Acosta - 23008203
# João Gabriel Biazon - 23004430





def chat(operation, user_email, password):
    recipient = input("Digite o e-mail do destinatário: ")
    message = input("Digite a mensagem: ")
    operation.send_message_to_db(user_email, recipient, message, password)

def ver_msg(operation, user_email, password):
    operation.check_received_messages(user_email, password)

def menu():
    print("-----Menu-----")
    print("1. Enviar Mensagem")
    print("2. Ler Mensagem")
    print("3. Sair")
    print("---------------")
    escolha = input("Escolha uma opção: ")
    return escolha

if __name__ == '__main__':

    operation = Operation()

    email, password = operation.login() #login usuario

    while True:
        escolha = menu()
        if escolha == '1':
            chat(operation, email, password)  #envia msg
        elif escolha == '2':
            ver_msg(operation, email, password) #ler msg enviadas
        elif escolha == '3':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")
