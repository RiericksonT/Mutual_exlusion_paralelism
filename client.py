import socket
import threading
import datetime
import os
import time

pid = os.getpid()

# Configurações do cliente
HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024

r = range(10)
k = 1
message_access = f'1|{pid}|00'
message_leave = f'3|{pid}|00'

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

# function to write in the file


def write_file(data):
    with open('resultado.txt', 'a') as file:
        file.write(data)


def aaa():
    for i in r:
        socket.send(message_access.encode('utf-8'))
        data = socket.recv(BUFFER_SIZE)
        print(data)
        if data.decode('utf-8').split('|')[0] == '2':
            print('Client is writing in the file')
            write_file(
                f'Client {pid} is writing in the file at {datetime.datetime.now()}\n')
            time.sleep(k)
            socket.send(message_leave.encode('utf-8'))
            print('Client has left the critical region')

        else:
            print("Client can't access the critical region, waiting...")
            time.sleep(k)
            continue


tred = threading.Thread(target=aaa)
tred.start()
