import socket
import threading
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234

uname = input("Enter user name::")

ip = input('Enter the IP Address::')

s.connect((ip, port))
s.send(uname.encode('ascii'))

clientRunning = True


def receive_msg(sock):
    server_down = False
    while clientRunning and (not server_down):
        try:
            msg = sock.recv(1024).decode('ascii')
            print(msg)
        except:
            print('Server is Down. You are now Disconnected. Press enter to exit...')
            server_down = True


threading.Thread(target=receive_msg, args=(s,)).start()

while clientRunning:
    tempMsg = input()
    msg = uname + '>>' + tempMsg
    if '**quit' in msg:
        clientRunning = False
        s.send('**quit'.encode('ascii'))
    else:
        s.send(msg.encode('ascii'))
