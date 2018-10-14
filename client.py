import os
import socket
import threading
from utils import bcolors as color
from utils import strings as text

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

uname = input(text.enter_name)

# ip = input('Enter the IP Address: ')
# port = int(input('Enter port number: '))

ip = '192.168.0.101'
port = 3001
s.connect((ip, port))
s.send(uname.encode('ascii'))

client_running = True

if not os.path.exists(uname):
    os.makedirs(uname)


def receive_msg(sock):
    server_down = False
    while client_running and (not server_down):

        try:
            msg = sock.recv(1024).decode('ascii')

            if msg == 'Recebendo arquivo...':
                print(text.recv_file)
                input_file = sock.recv(1024).decode('ascii')
                print(input_file)
                with open(os.path.join(uname, input_file), 'wb') as file_to_write:
                    while True:
                        data = sock.recv(1024)
                        if text.finish in str(data):
                            print(text.finish_download)
                            break
                        file_to_write.write(data)
                    file_to_write.close()

            elif text.cmd in msg:
                msg = msg[6:]
                print(color.OKBLUE + color.BOLD + msg + color.ENDC)

            elif '>>' in msg:
                aux = msg.split()[0]
                msg = msg[len(aux):]
                print(color.UNDERLINE + color.HEADER + aux + color.ENDC, end='')
                print(color.HEADER + msg + color.ENDC)

            else:
                print(msg)

        except Exception as e:
            print(text.server_down)
            print(e.with_traceback())
            server_down = True


threading.Thread(target=receive_msg, args=(s,)).start()

while client_running:

    temp_msg = input()
    msg = uname + '>>' + temp_msg

    if '--quit' in msg:
        clientRunning = False
        s.send('--quit'.encode('ascii'))

    elif '--help' in msg:
        print(text.help)

    elif '--file' in msg:

        inputFile = input(text.input_path)
        name_dest = input(text.input_dest)

        index = inputFile.rfind('/')
        fileName = inputFile[index + 1:]
        s.send(('--file' + fileName).encode('ascii'))

        with open(inputFile, 'rb') as file_to_send:
            for data in file_to_send:
                s.sendall(data)

        s.send(text.finish.encode('ascii'))
        s.send(name_dest.encode('ascii'))

    else:
        s.send(msg.encode('ascii'))
