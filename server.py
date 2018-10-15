import os
import socket
import threading
from utils import strings as text

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_running = True
ip = str(socket.gethostbyname(socket.gethostname()))
port = 3001

clients = {}

s.bind((ip, port))
s.listen()
print('UFAL-CHAT')
print('Use ::%s para se conectar.' % ip)

if not os.path.exists(text.dir_server):
    os.makedirs(text.dir_server)


def handle_client(client, uname):
    client_connected = True
    keys = clients.keys()

    while client_connected:
        try:
            msg = client.recv(1024).decode('ascii')
            response = text.online
            found = False

            if '--chatlist' in msg:
                client_no = 0
                for name in keys:
                    client_no += 1
                    response = response + str(client_no) + ' ' + name + ' $'
                client.send(response.encode('ascii'))

            elif '--file' in msg:
                input_file = msg.replace('--file', text.dir_server + '/')

                with open(input_file, 'wb') as file_to_write:
                    while True:
                        data = client.recv(1024)
                        if text.finish in str(data):
                            print(text.finish_download)
                            break
                        file_to_write.write(data)
                    file_to_write.close()

                destinator = str(data)[str(data).rfind('ACABOU')+6:-1]
                print(destinator)

                for name in keys:

                    if name == destinator:
                        clients.get(name).send(text.recv_msg_cmd.encode('ascii'))
                        clients.get(name).send(input_file[11:].encode('ascii'))

                        with open(input_file, 'rb') as file_to_send:
                            for data in file_to_send:
                                clients.get(name).sendall(data)

                        clients.get(name).send(text.finish.encode('ascii'))
                        found = True

                if not found:
                    client.send(text.invalid_dest.encode('ascii'))

            elif '--broadcast' in msg:
                msg = msg.replace('--broadcast', '')
                for k, v in clients.items():
                    v.send(msg.encode('ascii'))

            elif '--quit' in msg:
                client.send(text.exit.encode('ascii'))
                clients.pop(uname)
                print(uname + ' desconectou')
                client_connected = False

            else:
                for name in keys:
                    if ('--' + name) in msg:
                        msg = msg.replace('--' + name, '')
                        clients.get(name).send(msg.encode('ascii'))
                        found = True
                if not found:
                    client.send(text.invalid_dest.encode('ascii'))

        except Exception as e:
            clients.pop(uname)
            print(uname + ' foi desconectado, causa: ', end='')
            print(e)
            client_connected = False


while server_running:
    client, address = s.accept()
    uname = client.recv(1024).decode('ascii')
    print('%s conectou no chat' % str(uname))
    client.send(text.welcome.encode('ascii'))

    if client not in clients:
        clients[uname] = client
        threading.Thread(target=handle_client, args=(client, uname,)).start()
