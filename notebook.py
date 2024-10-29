# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 09:34:47 2018

@author: joungsuk
"""
"""
# protect
id = 2<<20;
cmd = 0x11 << 12
CanID = id + cmd

maxV = 4200
minV = 2000
maxI = 205000
minI = 0
maxCap = 200000
maxTemp = 50
delay = 0


print(hex(CanID))
print(hex(maxV))
print(hex(minV))
print(hex(maxI))
print(hex(minI))
print(hex(maxCap))
print(hex(maxTemp))
print(hex(delay))
"""
# OCV
id = 1<<20;
cmd = 0x06 << 12
CanID = id + cmd

interval = 10
endTime = 60000

print(hex(CanID))
print(hex(interval))
print(hex(endTime))

