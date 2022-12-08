import socket
import cv2
import imutils
from datetime import datetime
from Packet import *
from mpu6050 import mpu6050
import time
import serial
from time import sleep
import sys
from pulsesensor import Pulsesensor
import time

mpu = mpu6050(0x68)
ser = serial.Serial ("/dev/ttyS0")
p = Pulsesensor()
p.startAsyncBPM()

def main():
    try:
        # Socket Create
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()

        host_ip = '192.168.0.52' # socket.gethostbyname(host_name)

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
                    time_seconds = datetime.now().strftime('%H:%M:%S')

                    mpu_packet = str(mpu.get_all_data())
                    # read NMEA string received
                    gps_packet = str(ser.readline())
                    bpm_packet = ''
                    try:
                        bpm = p.BPM
                        if bpm > 0:
                            bpm_packet = str(bpm)
                        else:
                            bpm_packet = '0'
                    except:
                        p.stopAsyncBPM()

                    string_packet = mpu_packet + ' ' + gps_packet + ' ' + ' ' + bpm_packet + ' ' + time_seconds

                    packet = Packet(frame, string_packet)
                    data = packet.serialize()
                    a = pickle.dumps(data)
                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)

    except ConnectionResetError:
        print('Host has shutdown his interface')


if __name__ == "__main__":
    main()