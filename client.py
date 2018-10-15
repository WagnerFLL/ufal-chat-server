import os
import socket
from threading import Thread
import tkinter
from utils import strings as text

client_running = True

uname = ''


def receive():
    server_down = False
    while client_running and (not server_down):

        try:
            msg = client_socket.recv(1024).decode('ascii')

            if msg == 'Recebendo arquivo...':
                msg_list.insert(tkinter.END, 'Recebendo arquivo...')
                input_file = client_socket.recv(1024)
                data = input_file.replace(str(input_file)[2:str(input_file).find('\\')], '')
                input_file = str(input_file)[2:str(input_file).find('\\')]

                msg_list.insert(tkinter.END, input_file)
                with open(os.path.join(uname, input_file), 'wb') as file_to_write:
                    while True:
                        file_to_write.write(data)
                        data = client_socket.recv(1024)
                        if text.finish in str(data):
                            msg_list.insert(tkinter.END, text.finish_download)
                            break
                        file_to_write.write(data)
                    file_to_write.close()

            elif text.cmd in msg:
                msg = msg[6:]
                msg_list.insert(tkinter.END, msg)

            elif '>>' in msg:
                msg = msg.replace('>>', '')
                aux = msg.split()[0]
                msg = msg[len(aux):]
                msg_list.insert(tkinter.END, aux + ': ' + msg)

            else:

                if '$'in msg:
                    for x in str(msg).split('$'):
                        msg_list.insert(tkinter.END, x)
                else:

                    msg_list.insert(tkinter.END, msg)

        except Exception as e:
            print(text.server_down)
            print(e)
            server_down = True


def send(event=None):
    msg2 = my_msg.get()
    msg1 = my_msg2.get()
    msg = '--' + msg1 + ' ' + msg2
    msg = uname + '>>' + msg

    if len(msg2) > 0:
        msg_list.insert(tkinter.END, 'Você: ' + msg2)

    my_msg.set("")

    if '--quit' in msg:
        client_socket.send('--quit'.encode('ascii'))
        client_socket.close()
        top.quit()

    elif '--help' in msg:
        for x in text.help.split('$'):
            msg_list.insert(tkinter.END, x)

    elif '--file' in msg:
        file_input = msg2
        dest = msg1
        print('as ' + dest)
        index = file_input.rfind('/')
        file_name = file_input[index + 1:]
        client_socket.send(('--file' + file_name).encode('ascii'))

        with open(file_input, 'rb') as file_to_send:
            for data in file_to_send:
                client_socket.sendall(data)

        client_socket.send(text.finish.encode('ascii'))
        client_socket.send(dest.replace('file ', '').encode('ascii'))

    else:
        client_socket.send(msg.encode('ascii'))


def on_closing(event=None):
    my_msg.set("Tchau")
    send()


uname = input('Nome: ')
if not os.path.exists(uname):
    os.makedirs(uname)

top = tkinter.Tk()
top.title("Chat: " + uname)

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Mensagem")

my_msg2 = tkinter.StringVar()
my_msg2.set("Destinatario")

scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()

entry_field2 = tkinter.Entry(top, textvariable=my_msg2)
entry_field2.bind("<Return>", send)
entry_field2.pack()

send_button = tkinter.Button(top, text="Enviar", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '192.168.0.101'
port = 3001
client_socket.connect((ip, port))
client_socket.send(uname.encode('ascii'))

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
