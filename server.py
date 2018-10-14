import os
import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_running = True
ip = str(socket.gethostbyname(socket.gethostname()))
port = 3001

clients = {}

s.bind((ip, port))
s.listen()
print('Server Ready...')
print('Ip Address of the Server::%s' % ip)

if not os.path.exists('serverfile'):
    os.makedirs('serverfile')

def handle_client(client, uname):
    client_connected = True
    keys = clients.keys()

    while client_connected:
        try:
            msg = client.recv(1024).decode('ascii')
            response = 'Number of People Online\n'
            found = False
            if '--chatlist' in msg:
                client_no = 0
                for name in keys:
                    client_no += 1
                    response = response + str(client_no) + '::' + name + '\n'
                client.send(response.encode('ascii'))

            elif '--file' in msg:
                input_file = msg.replace('--file', 'serverfile/')

                with open(input_file, 'wb') as file_to_write:
                    while True:
                        data = client.recv(1024)
                        if 'ACABOU' in str(data):
                            print("Download finalizado.")
                            break
                        file_to_write.write(data)
                    file_to_write.close()

                destinator = client.recv(1024).decode('ascii')
                print(destinator)

                for name in keys:
                    if name == destinator:
                        clients.get(name).send('Recebendo arquivo...'.encode('ascii'))
                        clients.get(name).send(input_file[11:].encode('ascii'))
                        with open(input_file, 'rb') as file_to_send:
                            for data in file_to_send:
                                clients.get(name).sendall(data)

                        clients.get(name).send('ACABOU'.encode('ascii'))
                        found = True

                if not found:
                    client.send('Trying to send message to invalid person.'.encode('ascii'))

            elif '--broadcast' in msg:
                msg = msg.replace('**broadcast', '')
                for k, v in clients.items():
                    v.send(msg.encode('ascii'))
            elif '--quit' in msg:
                response = 'Stopping connection and exiting...'
                client.send(response.encode('ascii'))
                clients.pop(uname)
                print(uname + ' has been logged out')
                client_connected = False
            else:
                for name in keys:
                    if ('--' + name) in msg:
                        msg = msg.replace('--' + name, '')
                        clients.get(name).send(msg.encode('ascii'))
                        found = True
                if not found:
                    client.send('Trying to send message to invalid person.'.encode('ascii'))
        except Exception as e:
            print(e)
            clients.pop(uname)
            print(uname + ' has been logged out with except')
            client_connected = False


while server_running:
    client, address = s.accept()
    uname = client.recv(1024).decode('ascii')
    print('%s connected to the server' % str(uname))
    client.send('Welcome to Messenger. Type --help to know all the commands'.encode('ascii'))

    if client not in clients:
        clients[uname] = client
        threading.Thread(target=handle_client, args=(client, uname,)).start()
