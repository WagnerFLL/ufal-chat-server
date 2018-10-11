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


def handle_client(client, uname):
    client_connected = True
    keys = clients.keys()
    help = 'There are four commands in Messenger\n \
    1: --chatlist => gives you the list of the people currently online\n \
    2: --quit => To end your connection\n \
    3: --broadcast => To broadcast your message to each and every person currently present online\n \
    4: Add the name of the person in your message preceded by -- to send it to particular person'

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
            elif '--help' in msg:
                client.send(help.encode('ascii'))
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
        except:
            clients.pop(uname)
            print(uname + ' has been logged out')
            client_connected = False


while server_running:
    client, address = s.accept()
    uname = client.recv(1024).decode('ascii')
    print('%s connected to the server' % str(uname))
    client.send('Welcome to Messenger. Type --help to know all the commands'.encode('ascii'))

    if client not in clients:
        clients[uname] = client
        threading.Thread(target=handle_client, args=(client, uname,)).start()
