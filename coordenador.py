import datetime
import time
import socket
import threading
import os

pid = os.getpid()

# config coordenator
HOST = 'localhost'
PORT = 5000
BUFFER = 1024

# create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


lock = threading.Lock()

connections = []
queue = []
accessing_now = None

time_start = time.time()


class Semaphore:
    def __init__(self, value):
        self.value = value
        self.queue = []

    def acquire(self):
        self.queue.append(threading.current_thread())
        while self.queue[0] != threading.current_thread() or self.value == 0:
            pass
        self.value -= 1
        self.queue.pop(0)

    def release(self):
        self.value += 1


semaphore = Semaphore(1)

# function to write the log file


def write_file(data):
    with open('log.txt', 'a') as file:
        file.write(data)


# Algoritimo de exclusão mutua


def mutual_exclusion():
    global accessing_now

    while True:
        if len(queue) > 0:
            if accessing_now == None:
                semaphore.acquire()
                accessing_now = queue[0]
                queue.remove(queue[0])
                semaphore.release()


# function to receive new clients


def receive_new_clients(connection):
    global accessing_now
    global queue
    global time_start

    while True:
        try:
            if time.time() - time_start < 300:
                data = connection.recv(BUFFER).decode('utf-8').split('|')
                if data[0] == '1':
                    queue.append(connection)
                    write_file(
                        f'Client {data[1]} has solicited access to critical region at {datetime.datetime.now()}\n')

                    while accessing_now != connection:
                        continue

                    if connection:
                        write_file(
                            f'Client {data[1]} has access to critical region at {datetime.datetime.now()}\n')
                        connection.send(f'2|{pid}|00'.encode('utf-8'))

                        # start measuring time
                        time_start = time.time()

                elif data[0] == '3':
                    write_file(
                        f'Client {data[1]} has left the critical region at {datetime.datetime.now()}\n')
                    accessing_now = None
            else:
                accessing_now = None
                connection.close()
                # reset time
                time_start = time.time()
        except ConnectionResetError:
            continue


def terminal():
    global queue
    global accessing_now

    while True:
        command = input("1 - Show queue | 2 - Show accessing now | 3 - Exit\n")
        if command == '1':
            print(queue)
        elif command == '2':
            print(accessing_now)
        elif command == '3':
            break
        else:
            print('Invalid command')
            continue


term = threading.Thread(target=terminal)
term.start()

threadMut = threading.Thread(target=mutual_exclusion)
threadMut.start()

while True:
    client_socket, client_address = server.accept()
    connections.append(client_socket)
    threadRec = threading.Thread(
        target=receive_new_clients, args=([client_socket]))
    threadRec.start()
