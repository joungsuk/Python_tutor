# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import time

def Task200ms(port):
    port.write(b'\xFE')


def do_every(period, f, *args):
        def g_tick():
                t = time.time()
                count = 0
                while True:
                        count += 1
                        yield max(t + count * period - time.time(), 0)
        g = g_tick()
        while True:
                time.sleep(next(g))
                f(*args)


def get_acp():
    remain = ser.inWaiting()
    



ser = serial.Serial('COM5',baudrate=9600,timeout=1)




ser.write(b'\xF7')
time.sleep(0.2)
ser.write(b'\xFD')
time.sleep(0.2)

for i in range(30):
    ser.write(b'\xFE')
    time.sleep(0.2)
    print('send FE\n')

#880C0447CEC69A26C9
#880C04D9EF40F999C9
#7A080242842193
#7A080242842193
#ser.write(b'\x7A\x08\x02\x42\x84\x21\x93')
print('send shuntdown cmd\n')
    
ser.write(b'\x7A')
time.sleep(0.2)
ser.write(b'\x08')
time.sleep(0.2)
ser.write(b'\x02')
time.sleep(0.2)
ser.write(b'\x42')
time.sleep(0.2)
ser.write(b'\x84')
time.sleep(0.2)
ser.write(b'\x21')
time.sleep(0.2)
ser.write(b'\x93')
time.sleep(0.2)

for i in range(10):
    ser.write(b'\xFE')
    time.sleep(0.2)
    print('send FE\n')

ser.close()