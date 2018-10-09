import socket
import sys
from _thread import *


#-----------Mails-------------------------------------------------


def enviar_mensagem(user, destino, msg):
    fich = destino + '.txt'
    f = open(fich, 'a')
    f.writelines(user + '\n' + msg + '\n' + '-' + '\n')
    f.close()

def listar_mails(lista, listaAux):
    cad = ''
    indice = 0
    for mail in lista:
        if mail[2] == '+':
            listaAux.append(indice)
            cad = cad + mail[0] + '\n'
            cad = cad + mail[1] + '\n'
        indice += 1
    cad = cad[:-1] + ' '

    return cad

def ler_mails_naolidos(lista):
    cad = ''
    for mail in lista:
        if mail[2] == '-':
            cad = cad + mail[0] + '\n'
            cad = cad + mail[1] + '\n'
            mail[2] = '+'

    cad = cad[:-1] + ' '

    return cad


#----------Ficheiros----------------------------------------------


def atualizar_ficheiro_mails(user, lista, noti,  n):
    ver = False
    fich = user + '.txt'
    f = open(fich, 'r')
    for k in range(n):
        f.readline()
    for l in lista:
        for i in range(len(l)):
            f.readline()
    linha = f.readline()
    while linha:
        ver = True
        auxLista = []
        for i in range(3):
            auxLista.append(linha)
            auxLista[i] = auxLista[i].strip('\n')
            linha = f.readline()
        lista.append(auxLista)
        noti.append(auxLista)
    f.close()

    return ver

def ler_ficheiro_estado(dicio):
    f = open("estado.txt", 'r')
    linhas = f.readlines()

    for linha in linhas:
        line = linha.split()

        novo = {line[0]: line[1:]}
        dicio.update(novo)

    f.close()

def ler_ficheiro_conta(dicio):
    f = open("contas.txt", 'r')
    linhas = f.readlines()
    for linha in linhas:
        line = linha.split()
        inverte = line[3]
        novo = {line[1]: inverte[::-1]}
        dicio.update(novo)

    f.close()

def ler_ficheiro_mails(user):
    fich = user + '.txt'
    f = open(fich, 'r')
    linha = f.readline()
    lista = list()
    while linha:
        auxLista = []
        for i in range(3):
            auxLista.append(linha)
            auxLista[i] = auxLista[i].strip('\n')
            linha = f.readline()
        lista.append(auxLista)
    f.close()
    return lista

def escreve_ficheiro_conta(dicio):
    f = open("contas.txt", "w")
    for user, password in dicio.items():
        inverte = password
        f.writelines("User: " + user + " Password: " + inverte[::-1])
        f.writelines("\n")
    f.close()

def escrever_ficheiro_mails(user,lista):
    fich = user + '.txt'
    f = open(fich, 'w')
    for mail in lista:
        for linha in mail:
            f.writelines(linha + '\n')
    f.close()

def escreve_ficheiro_estado(dicio):
    f = open("estado.txt", "w")

    for user, estado in dicio.items():
        f.writelines(user + ' ' + estado[0] + ' ' + estado[1])
        f.writelines("\n")
    f.close()


#----------User-Pass----------------------------------------------


def verifica_user_pass(dicionario,user,password):
    if (dicionario.get(user,) == password):
        return True
    else:
        return False

def alterar_password(dicionario, user, password):
    dicionario.pop(user, )
    dicionario.setdefault(user, password)

def listar_clientes(dicio):
    cad = ''
    for cliente, estado in dicio.items():
        cad = cad + cliente + ',' + estado[0] + ','

    return cad[:-1]


#-------------------------------------------------------------------


#def encripta(palavra):


HOST = 'localhost'  # Symbolic name meaning all available interfaces
PORT = 9000  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed.')
    sys.exit()

print('Socket bind complete')

# Start listening on socket
s.listen(10)
print('Socket now listening')


dicio = dict()
estadoDicio = dict()
#listaMensagens = list()
# Function for handling connections. This will be used to create threads
def clientthread(conn):
    # Sending message to connected client
    conn.send("Bem-vindo ao server".encode())  # send only takes string

    # infinite loop so that function do not terminate and thread do not end.
    while True:
        # Receiving from client
        ler_ficheiro_conta(dicio)
        ler_ficheiro_estado(estadoDicio)
        n_msg_apagadas = 0
        user = conn.recv(1024).decode()
        if user in dicio.keys():
            conn.send("true".encode())
            password = conn.recv(1024).decode()
            if (verifica_user_pass(dicio, user, password)):
                conn.send("true".encode())
                estadoDicio[user][0] = 'on'
                escreve_ficheiro_estado(estadoDicio)
            else:
                conn.send("false".encode())
                while True:
                    user = conn.recv(1024).decode()
                    password = conn.recv(1024).decode()
                    if (verifica_user_pass(dicio, user, password)):
                        conn.send("true".encode())
                        estadoDicio[user][0] = 'on'
                        escreve_ficheiro_estado(estadoDicio)
                        break
                    else:
                        conn.send("false".encode())
        else:
            conn.send("false".encode())
            while True:
                user = conn.recv(1024).decode()
                password = conn.recv(1024).decode()
                if (verifica_user_pass(dicio,user,password)):
                    conn.send("true".encode())
                    estadoDicio[user][0] = 'on'
                    escreve_ficheiro_estado(estadoDicio)
                    break
                else:
                    conn.send("false".encode())

        listaMensagens = ler_ficheiro_mails(user)
        print('com o username de '+user)
        while True:
            ler_ficheiro_estado(estadoDicio)
            listaNotifica = list()

            if atualizar_ficheiro_mails(user, listaMensagens, listaNotifica, n_msg_apagadas):
                conn.send('notificar,'.encode())
                if len(listaNotifica) == 1:
                    notificar = 'Recebeu uma mensagem de ' + listaNotifica[0][0]
                    conn.send(notificar.encode())
                else:
                    notificar = 'Recebeu ' + str(len(listaNotifica)) + ' mensagens'
                    conn.send(notificar.encode())

            conn.send(',menu'.encode())
            menu_item = conn.recv(1024).decode()

            if menu_item == '1':
                msg = ler_mails_naolidos(listaMensagens)
                conn.send(msg.encode())

            if menu_item == '2':
                clientesLista = listar_clientes(estadoDicio)
                conn.send(clientesLista.encode())

            while menu_item == '3':
                destino = conn.recv(1024).decode()
                if destino in dicio.keys():
                    conn.send("true".encode())
                    msg = conn.recv(1024).decode()
                    if destino == user:
                        aux = []
                        aux.append(user)
                        aux.append(msg)
                        aux.append('-')
                        listaMensagens.append(aux)
                        break

                    else:
                        enviar_mensagem(user, destino, msg)
                        break
                else:
                    conn.send("false".encode())

            if menu_item == '4':
                msg = listar_mails(listaMensagens, list())
                conn.send(msg.encode())

            while menu_item == '5':
                listaAux = list()
                mails = listar_mails(listaMensagens, listaAux)
                conn.send(mails.encode())
                if not listaAux:
                    break
                else:
                    escolha = conn.recv(1024).decode()
                    iescolha = int(escolha)
                    if iescolha <= (len(listaAux)):
                        listaMensagens.pop(listaAux[iescolha - 1])
                        n_msg_apagadas += 1
                        conn.send('true'.encode())
                        break
                    else:
                        conn.send('false'.encode())

            while menu_item == '6':
                atual = conn.recv(1024).decode()
                pass1 = conn.recv(1024).decode()
                conn.send('n'.encode())
                pass2 = conn.recv(1024).decode()

                if dicio[user] == atual and pass1 == pass2:
                    alterar_password(dicio, user, pass1)
                    conn.send("true".encode())
                    break
                else:
                    conn.send("false".encode())

            while menu_item == '7':
                if estadoDicio[user][1] == 'admin':
                    msg = 'true'
                    conn.send(msg.encode())
                    op = conn.recv(1024).decode()
                    if op == '1':
                        cli = conn.recv(1024).decode()
                        if cli in dicio.keys() and estadoDicio[cli][1] == 'user':
                            estadoDicio[cli][1] = 'admin'
                            escreve_ficheiro_estado(estadoDicio)
                            conn.send("true".encode())
                        else:
                            conn.send("false".encode())
                        break
                    if op == '2':
                        cli = conn.recv(1024).decode()
                        if cli in dicio.keys() and estadoDicio[cli][1] == 'user':
                            conn.send("true".encode())
                            pw = conn.recv(1024).decode()
                            dicio[cli] = pw
                            escreve_ficheiro_conta(dicio)
                        else:
                            conn.send("false".encode())
                        break
                    if op == '3':
                        cli = conn.recv(1024).decode()
                        if cli not in dicio.keys():
                            conn.send("true".encode())
                            pw = conn.recv(1024).decode()
                            dicio.update({cli: pw})
                            estadoDicio.update({cli: ['off', 'user']})
                            escreve_ficheiro_conta(dicio)
                            fich = cli + '.txt'
                            f = open(fich, 'w')
                            f.close()
                        else:
                            conn.send("false".encode())
                        break

                else:
                    msg = 'false'
                    conn.send(msg.encode())
                    break

            while menu_item == '8':
                destino = conn.recv(1024).decode()
                listaDestinos = destino.split(',')
                ver = 0
                for cliente in listaDestinos:
                    if not cliente in dicio.keys():
                        ver = 1
                if ver == 0:
                    conn.send('true'.encode())
                    msg = conn.recv(1024).decode()
                    for cliente in listaDestinos:
                        if cliente == user:
                            aux = list()
                            aux.append(user)
                            aux.append(msg)
                            aux.append('-')
                            listaMensagens.append(aux)
                        else:
                            enviar_mensagem(user, cliente, msg)
                    break
                else:
                    conn.send('false'.encode())


            if menu_item == '0':
                break

            else:
                pass
        if menu_item == '0':
                break

    estadoDicio[user][0] = 'off'
    escreve_ficheiro_estado(estadoDicio)
    escreve_ficheiro_conta(dicio)
    escrever_ficheiro_mails(user, listaMensagens)
    # came out of loop
    print("cliente "+ user + " saiu!")
    conn.close()


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]),end = ' ')

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))

s.close()

#----------------------------------------------------------------------------------------

