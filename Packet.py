import pickle
import struct

class Packet:
    def __init__(self, video_frame, data_list):
        self.video_frame = video_frame
        self.data_list = data_list

    def serialize(self):
        return [self.video_frame, self.data_list]

    def unserialize(self):
        return pickle.loads(self)

    def get_video(self):
        return self.video_frame

    def get_data_list(self):
        return self.data_list
