import pickle
import socket
from threading import Thread

from flask import Flask, request
from processor import *
from daoModel import *

app = Flask(__name__)

PORT = 5005
HOST = "127.0.0.1"

def handle_client(conn, addr):
    with conn:
        temp = conn.recv(1024)

        data = pickle.loads(temp)
        if type(data) is TransportData:
            match data.type:
                case TransportType.REGISTER:
                    msg = register(data.data)
                
                case TransportType.LOGIN:
                    msg = StatusCode.INTERNAL_SERVER_ERROR
                    

            print(msg.name)
            resopnse = pickle.dumps(msg.name)
            conn.sendall(resopnse)

        else:
            resopnse = pickle.dumps(StatusCode.INTERNAL_SERVER_ERROR.name)
            conn.sendall(resopnse)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Listening...')

        while True:
            conn, addr = s.accept()
            new_thread = Thread(target=handle_client, args=(conn, addr))
            new_thread.start()

if __name__ == '__main__':
    main()