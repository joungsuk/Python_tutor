# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 19:07:48 2019

@author: joungsuk
"""
import struct

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def double_to_hex(f):
    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])

def hex_to_float(h):
    return struct.unpack('!f', bytes.fromhex(h))

