import socket
import sys
import os

def menu():
    print("1 - LIST_MESS", end=' | ')
   # print("\t Lista mensagens por ler\n",)
    print("2 - LIST_USERS", end=' | ')
    #print("\t Lista todos os clientes autorizados\n")
    print("3 - SEND_MESS", end=' | ')
    #print("\t Envia uma mensagem para um cliente autorizado\n")
    print("4 - LIST_READ", end=' | ')
    #print("\t Lista todas as mensagens já lidas\n")
    print("5 - REMOVE_MES", end=' | ')
    #print("\t Apaga mensagens\n")
    print("6 - CHANGE_PASSW", end=' | ')
    #print("\t Altera a password\n")
    print("7 - OPER", end=' | ')
    #print("\t Alterar os privilégios do cliente\n")
    print("8 - SEND_MULTI", end=' | ')
    # print("\t Envia uma mensagem a varios clientes\n")
    print("a - UPDATE", end=' | ')
    #print("\t Atualiza serviço de mensagens\n")
    print("0 - QUIT\n")
    #print("\t Abandona o sistema\n")


def login():
    user = input("User: ")
    password = input('Password: ')
    sock.send(user.encode())
    sock.send(password.encode())

    data = sock.recv(1024).decode()
    if data == 'true':
        return True
    else:
        print("\n\t*Erro no login! Tente outra vez!*\n")
        return False

if __name__ == '__main__':
    clear = lambda: os.system('cls')

    host = 'localhost'
    port = int(sys.argv[1])

    # cria socket e conectar ao server   sever TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((host, port))

    while True:
        data = sock.recv(1024).decode()
        print(data)
        arg_user = str(sys.argv[2])
        sock.send(arg_user.encode())
        ver = sock.recv(1024).decode()
        if ver == 'true':
            arg_pass = str(sys.argv[3])
            sock.send(arg_pass.encode())
            data = sock.recv(1024).decode()
        if data == 'false':
            while True:
                print('\n\t*Erro no login! Tente outra vez*\n')
                if login():
                    break
        print('\nAcedeu à sua conta')
        input('\n\t\t*Enter para continuar*\n')

        while True:

            server_msg = sock.recv(1024).decode()
            noti = server_msg.split(',')

            menu()
            if noti[0] == 'notificar':
                print('\n\t*' + noti[1] + '*\n')

            menu_item = str(input("Selecione uma opção: "))
            sock.send(menu_item.encode())
            if menu_item == '1':
                print('Lista de Mensagens não lidas...')
                mensagens_nl = sock.recv(1024).decode()
                if mensagens_nl == ' ':
                    print('\n\t*Não tem nenhuma mensagem por ler*\n')
                else:
                    listaMensagens = mensagens_nl.split('\n')
                    for i in range(len(listaMensagens)):
                        if i % 2 == 0:
                            print('\n\tRemetente: ' + listaMensagens[i])
                        else:
                            print('\tMensagem: ' + listaMensagens[i])
                    print('\n')
                input('\n\t\t*Enter para continuar*\n')
                clear()

            if menu_item == '2':
                clientes = sock.recv(1024).decode()
                listaClientes = clientes.split(',')
                print("Lista de Clientes...\n")
                for i in range(0, len(listaClientes), 2):
                    print('\t-> '+listaClientes[i]+' ('+listaClientes[i+1]+')')
                print('\n')
                input('\n\t\t*Enter para continuar*\n')
                clear()

            while menu_item == '3':
                print("Enviar mensagem...\n")
                destino = input("Destinatário: ")
                sock.send(destino.encode())
                data = sock.recv(1024).decode()
                if data == 'true':
                    msg = input("Escreve a sua mensagem: ")
                    sock.send(msg.encode())
                    print("\n\t*Mensagem enviada com sucesso*\n")
                    input('\n\t\t*Enter para continuar*\n')
                    clear()
                    break
                else:
                    print("\n\t*Destinatário não existe, tente outra vez!*\n")
                input('\n\t\t*Enter para continuar*\n')
                clear()

            if menu_item == '4':
                print('Lista de Mensagens lidas...')
                mensagens_l = sock.recv(1024).decode()
                if mensagens_l == ' ':
                    print('\n\t*Não tem nenhuma mensagem lida*\n')

                else:
                    listaMensagens = mensagens_l.split('\n')
                    for i in range(len(listaMensagens)):
                        if i % 2 == 0:
                            print('\n\tRemetente: ' + listaMensagens[i])
                        else:
                            print('\tMensagem: ' + listaMensagens[i])
                    print('\n')
                input('\n\t\t*Enter para continuar*\n')
                clear()

            while menu_item == '5':
                print('Lista de Mensagens...')
                mensagem = sock.recv(1024).decode()
                if mensagem == ' ':
                    print('\n\t*Não tem mensagens para eliminar*\n')
                    input('\n\t*Enter para continuar*\n')
                    clear()
                    break
                indice = 1
                listaMensagens = mensagem.split('\n')
                for i in range(len(listaMensagens)):
                    if i % 2 == 0:
                        print('\nMensagem ' + str(indice) + ':')
                        print('\tRemetente: ' + listaMensagens[i])
                        indice += 1
                    else:
                        print('\tMensagem: ' + listaMensagens[i])
                escolha = input("\nQual mensagem que quer eliminar: ")
                sock.send(escolha.encode())
                data = sock.recv(1024).decode()
                if data == 'true':
                    print('\n\t*Mensagem eliminado com sucesso*\n')
                    input('\n\t\t*Enter para continuar*\n')
                    clear()
                    break
                else:
                    print('\n\t*Ocorreu um erro!Tente outravez*\n')
                input('\n\t\t*Enter para continuar*\n')
                clear()

            while menu_item == '6':
                print('Alterar a Password...\n')
                password = input('Atual Password: ')
                novapass1 = input("Nova password: ")
                novapass2 = input("Confirmar password: ")

                sock.send(password.encode())
                sock.send(novapass1.encode())
                sock.recv(1024)
                sock.send(novapass2.encode())
                data = sock.recv(1024).decode()
                if data == 'true':
                    print("\t*Password alterada com sucesso!*\n")
                    input('\n\t\t*Enter para continuar*\n')
                    clear()
                    break
                else:
                    print("\t*Erro! Tente outra vez!*\n")
                input('\n\t\t*Enter para continuar*\n')
                clear()

            while menu_item == '7':
                acesso = sock.recv(1024).decode()
                if acesso == 'false':
                    print('\n\t\t*Erro no acesso!*\n\t*Não tem permissão para entrar*\n')
                    input('\n\t\t*Enter para continuar*\n')
                    clear()
                    break
                else:
                    print('\n1 - Alterar priviléligo de um cliente(user)\n\n2 - Alterar password de um cliente(user)\n\n3 - Criar uma conta\n')
                    op = input('Escolha um opção: ')
                    sock.send(op.encode())
                    if op == '1':
                        cli = input('Cliente que pretende dar Admin: ')
                        sock.send(cli.encode())
                        resp = sock.recv(1024).decode()
                        if resp == "true":
                            print('\n\t*Permissão concedida*\n')
                        else:
                            print('\n\t*Erro na permissão, volte ao menu*\n')
                        input('\n\t\t*Enter para continuar*\n')
                        clear()
                        break

                    if op == '2':
                        cli = input('Cliente que pretende alterar a password: ')
                        sock.send(cli.encode())
                        resp = sock.recv(1024).decode()
                        if resp == "true":
                            pw = input('Nova password: ')
                            sock.send(pw.encode())
                            print('\n\t*Password alterada com sucesso*\n')
                        else:
                            print('\n\t*Erro no cliente, volte ao menu*\n')
                        input('\n\t\t*Enter para continuar*\n')
                        clear()
                        break
                    if op == '3':
                        print('\nCriar conta...')
                        cli = input('\tUsername: ')
                        sock.send(cli.encode())
                        resp = sock.recv(1024).decode()
                        if resp == "true":
                            pw = input('\tPassword: ')
                            sock.send(pw.encode())
                            print('\n\t*Cliente criado con sucesso*\n')
                        else:
                            print('\n\t*Erro, cliente já tem conte*\n')

                        input('\n\t\t*Enter para continuar*\n')
                        clear()
                        break
                    elif op not in '123' and op not in '321':
                        print('\n\t*Opçao Invalida, volte ao menu*\n')
                        input('\n\t\t*Enter para continuar*\n')
                        clear()

            while menu_item == '8':
                print("Enviar mendagem...")
                lista_destino = input("Destinatários(separados por virgúlas): ")
                sock.send(lista_destino.encode())
                data = sock.recv(1024).decode()
                if data == 'true':
                    msg = input("Escreve a sua mensagem: ")
                    sock.send(msg.encode())
                    print("\n\t*Mensagem enviada com sucesso*\n")
                    input('\n\t\t*Enter para continuar*\n')
                    clear()
                    break
                else:
                    print("\n\t*Erro nos Destinatários, tente outra vez!*\n")
                input('\n\t\t*Enter para continuar*\n')
                clear()

            if menu_item == 'a':
                clear()
                print('\n\t\t*Atualizado*\n')
                pass

            while menu_item == '0':
                clear()
                print('\n\t*Sessão terminada!*\n')
                sock.close()
                exit(0)
                break

            if menu_item == '\n' and menu_item not in '1a234568790' and menu_item not in '0a987654321':

                print("\n\t*Opção invalida, tente outra vez*\n")
                input('\n\t\t*Enter para continuar*\n')
                clear()
                pass

