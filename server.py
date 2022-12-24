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
ser = serial.Serial("/dev/ttyAMA0")
p = Pulsesensor()
p.startAsyncBPM()

def gps_read():
    count = 6
    gps_packet = ''
    while count > 0:
        # read NMEA string received
        temp_line = str(ser.readline())
        #temp_line.decode('utf-8')
        gps_packet += temp_line
        count -= 1
    return gps_packet

def main():
    try:
        # Socket Create
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()

        host_ip = '192.168.1.13' # socket.gethostbyname(host_name)

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
                    bpm_packet = ''
                    try:
                        bpm = p.BPM
                        if bpm > 0:
                            bpm_packet = str(bpm)
                        else:
                            bpm_packet = '0'
                    except:
                        p.stopAsyncBPM()

                    string_packet = mpu_packet + ' ' + gps_read() + ' ' + ' ' + bpm_packet + ' ' + time_seconds

                    packet = Packet(frame, string_packet)
                    data = packet.serialize()
                    a = pickle.dumps(data)
                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)

    except ConnectionResetError:
        print('Host has shutdown his interface')


if __name__ == "__main__":
    main()