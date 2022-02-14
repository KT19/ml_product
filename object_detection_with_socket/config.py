#-*-coding:utf-8-*-
"""
Config file for socket
"""

class Config:
    header = 128
    port = 8080
    buffer_size = 1024 #buffer size to receive data
    format = "utf-8"
    server_ip = "localhost" #set ip addr for server

cfg = Config()
