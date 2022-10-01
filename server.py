import socket, cv2, pickle, struct, imutils
import logging
import threading
import time
from datetime import datetime
from Packet import *

def data_transmission():
    try:
        # Socket Create
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_ip = '192.168.100.200' # socket.gethostbyname(host_name)
        print('HOST IP:', host_ip)
        port = 9999
        socket_address = (host_ip, port)
        # Socket Bind
        server_socket.bind(socket_address)
        # Socket Listen
        server_socket.listen(5)
        print("LISTENING AT:", socket_address)

        # Socket Accept
        while True:
            client_socket, addr = server_socket.accept()
            print('GOT CONNECTION FROM:', addr)
            if client_socket:
                vid = cv2.VideoCapture(0)
                while vid.isOpened():
                    img, frame = vid.read()
                    frame = imutils.resize(frame, width=480)
                    time_seconds = datetime.now().strftime('%S')
                    packet = Packet(frame, time_seconds)
                    data = packet.serialize()
                    a = pickle.dumps(data)
                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)

                    #cv2.imshow('TRANSMITTING VIDEO', data[0])
                    if cv2.waitKey(1) & 0xFF == ord('x'):
                        client_socket.close()
    except ConnectionResetError:
        print('Host has shutdown his interface')

def main():
    data_th = threading.Thread(target=data_transmission(), args=(1,), daemon=True)
    data_th.start()

if __name__ == "__main__":
    main()
