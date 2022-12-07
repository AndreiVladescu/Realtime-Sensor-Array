import socket
import cv2
import imutils
from datetime import datetime
from Packet import *
from mpu6050 import mpu6050
import time

mpu = mpu6050(0x68)

def main():
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
                    frame = imutils.resize(frame, width=640)
                    time_seconds = datetime.now().strftime('%S')

                    mpu_packet = str(mpu.get_all_data())

                    packet = Packet(frame, mpu_packet)
                    data = packet.serialize()
                    a = pickle.dumps(data)
                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)

    except ConnectionResetError:
        print('Host has shutdown his interface')


if __name__ == "__main__":
    main()
