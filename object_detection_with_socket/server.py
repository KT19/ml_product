#-*-coding:utf-8-*-
import socket
import threading
import time
import numpy as np
import cv2
import json
#read config
from config import cfg
#set object detector
from object_detector import ObjectDetector
detector = ObjectDetector()

#set server host
SERVER = socket.gethostbyname(socket.gethostname()) #set host ip addr
ADDR = (SERVER, cfg.port)

#creating socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #data streaming
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR) #bind

def object_detection(data, thres=0.5):
    pred = detector(data) #return dict
    obj_num = len(pred["scores"])

    output = []
    for i in range(obj_num):
        if pred["scores"][i] < thres:
            continue

        bbox = pred["boxes"][i]
        temp = {
        "class_idx": pred["labels"][i].item(),
        "class_name": detector.label2cat(pred["labels"][i].item()),
        "bbox": [bbox[0].item(), bbox[1].item(), bbox[2].item(), bbox[3].item()]}

        obj = "obj"+str(i)
        output.append(temp)
    print(output)

    return output

def process(connection, addr):
    def get_data_from_client():
        #get message header first
        msg_header = connection.recv(cfg.header).decode(cfg.format) #wait till get data
        if not msg_header:
            return None
        msg_length, height, width, channel, _ = msg_header.split(":")

        msg_length = int(msg_length)
        height = int(height)
        width = int(width)
        channel = int(channel)

        print("Message length:{}".format(msg_length))
        msg_length = int(msg_length) #get length of message

        #message contents
        msg = {}
        received_size = 0
        received_data = b""

        #get all img data
        while True:
            try:
                data = connection.recv(cfg.buffer_size)
                received_size += len(data) #add data size
                received_data += data #add data

                if received_size >= msg_length:
                    break

            except Exception as e:
                print("Error in server during receiving data")
                print(e)

        msg["expected_received_size"] = msg_length
        msg["actual_received_size"] = received_size
        msg["data"] = np.frombuffer(received_data, np.uint8).reshape((height, width, channel)) #from byte to array

        assert msg_length == received_size, "Some data might be lost"

        return msg


    eoc_flag = False
    while not eoc_flag:
        msg = get_data_from_client() #wait until get data
        if msg is None:
            continue

        eoc_flag = True
        print(msg["data"].shape)

        s_time = time.time()
        res = object_detection(msg["data"])
        e_time = time.time()
        print("Elapsed time: {}[sec]".format(e_time - s_time))

        #send data
        res = json.dumps(res).encode(cfg.format) #convert to byte
        #send header of the data
        header = (str(len(res))+":").encode(cfg.format)
        header += b' '*(cfg.header - len(header)) #adjust format
        connection.send(header)
        connection.send(res)

    connection.close()
    print("connection is closed")

def start():
    server.listen() #listen
    print("server ip:{}, server port:{}".format(ADDR[0], ADDR[1]))
    while True:
        connection, addr = server.accept() #wait
        print(connection)
        thread = threading.Thread(target=process, args=(connection, addr))
        thread.start()
        print("Now {} connections".format(threading.activeCount() - 1))

if __name__ == "__main__":
    print("Launch server...")
    start()
