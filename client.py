import os
import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

uname = input("Enter user name: ")

# ip = input('Enter the IP Address: ')
ip = '192.168.0.101'
# port = int(input('Enter port number: '))
port = 3001
s.connect((ip, port))
s.send(uname.encode('ascii'))

client_running = True

help = '\033[93m' + 'Comandos para o chat:\n \
    1: --chatlist => lista todos os usuários ativos\n \
    2: --quit => Sai da aplicação\n \
    3: --broadcast => Envia mensagem para todos que estiverem online\n \
    4: --UserName para enviar uma mensagem privada' + '\033[0m'

if not os.path.exists(uname):
    os.makedirs(uname)

def receive_msg(sock):
    server_down = False
    while client_running and (not server_down):

        try:
            msg = sock.recv(1024).decode('ascii')
            print(msg)

            if msg == 'Recebendo arquivo...':

                input_file = sock.recv(1024).decode('ascii')
                print(input_file)
                with open(os.path.join(uname, input_file), 'wb') as file_to_write:
                    while True:
                        data = sock.recv(1024)
                        if 'ACABOU' in str(data):
                            print("Download finalizado.")
                            break
                        file_to_write.write(data)
                    file_to_write.close()

        except:
            print('Server is Down. You are now Disconnected. Press enter to exit...')
            server_down = True


threading.Thread(target=receive_msg, args=(s,)).start()

while client_running:

    temp_msg = input()
    msg = uname + '>>' + temp_msg

    if '--quit' in msg:
        clientRunning = False
        s.send('--quit'.encode('ascii'))

    elif '--help' in msg:
        print(help)

    elif '--file' in msg:

        inputFile = input('Digite o caminho para o arquivo: ')
        name_dest = input('Destinatário: ')

        index = inputFile.rfind('/')
        fileName = inputFile[index + 1:]
        s.send(('--file' + fileName).encode('ascii'))

        with open(inputFile, 'rb') as file_to_send:
            for data in file_to_send:
                s.sendall(data)

        s.send('ACABOU'.encode('ascii'))
        s.send(name_dest.encode('ascii'))

    else:
        s.send(msg.encode('ascii'))
