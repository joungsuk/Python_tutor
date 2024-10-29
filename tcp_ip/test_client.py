# -*- coding: utf-8 -*-
"""
Created on Fri May 29 11:30:16 2020

@author: jslee
"""

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.50', 80))

