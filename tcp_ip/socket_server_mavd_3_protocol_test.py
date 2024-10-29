# -*- coding: utf-8 -*-
"""
Created on Thu May 28 14:42:11 2020

@author: jslee
"""

import socket
import struct
import numpy as np

# 접속할 서버 주소입니다. 여기에서는 루프백(loopback) 인터페이스 주소 즉 localhost를 사용합니다. 
HOST = '192.168.1.7'

# 클라이언트 접속을 대기하는 포트 번호입니다.   
PORT = 5002        


# 소켓 객체를 생성합니다. 
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 포트 사용중이라 연결할 수 없다는 
# WinError 10048 에러 해결를 위해 필요합니다. 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
# HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
# 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다. 
# PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.  
#server_socket.bind((HOST, PORT))
server_socket.bind((socket.gethostname(), PORT))

# 서버가 클라이언트의 접속을 허용하도록 합니다. 
print('waiting client')
server_socket.listen()

# accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다. 
client_socket, addr = server_socket.accept()

# 접속한 클라이언트의 주소입니다.
print('Connected by', addr)

#client_socket.settimeout(5.0)

length = None
buffer = bytes([])
step = 0
stx = bytes([0x02, 0xfe])
etx = bytes([0x03])

cmdVersion = stx + bytes([0x01, 0x00, 0x7E, 0x7F]) + etx
cmdUpdate = stx + bytes([0x05, 0x00, 0x7F, 0x5A, 0x72, 0xC3, 0x12, 0x25]) + etx
#cmdCal1_big = stx + bytes([0x09, 0x00, 0x42, 0, 0, 0, 0, 0x45, 0x68, 0x8f, 0xfc, 0x00]) + etx #big endian

v_zero = np.float32(2048.0).tobytes()
v_span = np.float32(4500.0).tobytes()

cmdCalZero = stx + bytes([0x09, 0x00, 0x42, 0x00, 0x00, 0, 0]) + v_zero + bytes([0x90]) + etx #little enditan
cmdCalSpan = stx + bytes([0x09, 0x00, 0x42, 0x01, 0x01, 0, 0]) + v_span + bytes([0xBE]) + etx #little enditan

#  client_socket.sendall(cmdVersion)

# 무한루프를 돌면서 
"""
while True:

    # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다. 
    rcv_data = client_socket.recv(2000)

    # 빈 문자열을 수신하면 루프를 중지합니다. 
    if not rcv_data:
        print('client socket close')
        break
    
    print("patch len = %d\n" %(len(rcv_data)))


    if length is None:
        if stx not in rcv_data:
           continue

        buffer = bytes([])
        pos_stx = rcv_data.find(stx)

        length = int.from_bytes(rcv_data[pos_stx + 2:pos_stx + 4], byteorder="little") + 6
        print("packet len = %d\n" %(length))
        step = 0
        buffer += rcv_data[pos_stx:]
        print("s%d len = %d, %d\n" %(step, len(rcv_data), len(buffer)))
        print(bytes(buffer).hex())
        continue
        
    else:
        length = None
        buffer = bytes([])
        continue
"""

"""
    buffer += data
    while True:
        if length is None:
            if "\0x02\0xfe" not in buffer:
                break
             # remove the length bytes from the front of buffer
             # leave any remaining bytes in the buffer!
             length_str, ignored, buffer = buffer.partition('\0x02\0xfe')
             length = int(length_str)

        if len(buffer) < length:
            break
        
        message = buffer[:length]
        buffer = buffer[length:]
        length = None
        # 수신받은 문자열을 출력합니다.
        print(message[0:4])
    
    # 받은 문자열을 다시 클라이언트로 전송해줍니다.(에코) 
    #client_socket.sendall(data)
"""

# 소켓을 닫습니다.
#client_socket.close()
#server_socket.close()