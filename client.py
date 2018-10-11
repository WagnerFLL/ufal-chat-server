import socket
import threading
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

uname = input("Enter user name: ")

ip = input('Enter the IP Address: ')

port = int(input('Enter port number: '))

s.connect((ip, port))
s.send(uname.encode('ascii'))

client_running = True


def receive_msg(sock):
    server_down = False
    while client_running and (not server_down):
        try:
            msg = sock.recv(1024).decode('ascii')
            print(msg)
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
    else:
        s.send(msg.encode('ascii'))
