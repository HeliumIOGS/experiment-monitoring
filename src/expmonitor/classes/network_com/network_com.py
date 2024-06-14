#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Jun 13 17:29:00 2024

@author: tc
"""

# Standard library imports:
import socket
import time

class NetworkCom():

    def __init__(self, port):
        self.buffer_size = 1024
        self.num_prec = 6
        self.conversion_fctn = lambda t: t ## No conversion
        self.IP = '10.117.53.15'  # Static IP: IOGS network (Galluzzo)
        self.port = port  # Match to server side port

    def connect(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((self.IP, self.port))
        self.soc.sendall(b'a')  # Send a non-empty message to initialize TCP/IP

    def measure(self):
        value = float(self.soc.recv(self.buffer_size).decode())
        value = round(self.conversion_fctn(value), self.num_prec)

        # Buffer time:
        time.sleep(0.1)
        return value

    def disconnect(self):
        self.soc.shutdown(socket.SHUT_RDWR)
        self.soc.close()

# Execution:
if __name__ == '__main__':

    network_com = NetworkCom(6666)
    network_com.connect()
    value = network_com.measure()
    network_com.disconnect()
    print(value)
