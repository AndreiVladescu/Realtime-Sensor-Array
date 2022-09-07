import socket, cv2, pickle, struct
import logging
import threading
import time
from Packet import *

def data_receiving():
    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '192.168.1.10'  # paste your server ip address here
    port = 9999
    client_socket.connect((host_ip, port))  # a tuple
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        # Reading the necessary message length
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        # Reading the actual data
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        unserialised_data = pickle.loads(frame_data)
        packet = Packet(unserialised_data[0], unserialised_data[1])

        frame = packet.get_video()
        cv2.imshow("RECEIVING VIDEO", frame)
        print(packet.get_data_list())
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    client_socket.close()

def main():
    data_th = threading.Thread(target=data_receiving(), args=(1,), daemon=True)
    data_th.start()

if __name__ == "__main__":
    main()