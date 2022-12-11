import pickle
import socket
from threading import Thread
from dtoModel import *

def send_registration(data, host, port):
    message = TransportData(TransportType.REGISTER, data)
    
    return send_data(message, host, port)


def send_data(data, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        send_data = pickle.dumps(data)
        s.connect((host, port))
        s.sendall(send_data)
        temp = s.recv(1024)
        response = pickle.loads(temp)

    return response