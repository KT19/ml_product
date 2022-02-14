#-*-coding:utf-8-*-
import socket
import numpy as np
import json
#read config
from config import cfg

#create socket
class SocketAgent:
    def __init__(self, dst_ip=None, dst_port=None):
        assert dst_ip != None, "need to set dst ip"
        assert dst_port != None, "need to set dst port"

        ADDR = (dst_ip, dst_port) #set ip & port
        self.agent = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #send streaming
        self.agent.connect(ADDR)

    def send(self, data):
        def create_header(length, h, w, c):
            return str(length)+":"+str(h)+":"+str(w)+":"+str(c)+":"

        #initial setup
        height, width, channel = data.shape
        message = data.tobytes() #encode data
        msg_length = create_header(len(message), height, width, channel).encode(cfg.format) #encode data

        header = msg_length + b' ' * (cfg.header - len(msg_length)) #adjust format

        self.agent.send(header)
        self.agent.send(message)
        print("data is send")


    def get(self):
        rec_header = self.agent.recv(cfg.header).decode(cfg.format) #wait till get data
        msg_length,_ = rec_header.split(":")
        msg_length = int(msg_length)
        print("received data size {}".format(msg_length))

        #message contents
        msg = {}
        received_size = 0
        received_data = b""

        #get all data
        while True:
            try:
                data = self.agent.recv(cfg.buffer_size)
                received_size += len(data) #add data size
                received_data += data #add data
                if received_size >= msg_length:
                    break

            except Exception as e:
                print("Error in socket agent during receiving data")
                print(e)

        msg["expected_received_size"] = msg_length
        msg["actual_received_size"] = received_size
        msg["data"] = json.loads(received_data.decode(cfg.format))

        assert msg_length == received_size, "some data might be lost during receiving data from the server"

        return msg
