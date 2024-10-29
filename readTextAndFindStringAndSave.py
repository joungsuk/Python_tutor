# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:01:33 2020

@author: jslee
"""

f = open("20200106 discharge 2-1.txt", "r")
fsave = open("extract6.txt", "w")
lines = f.readlines()

f.close();

"""
for line in lines:
    if "6A9000" in line:
        line = line.replace(" (8) Ext", "")
        line = line.replace(" : ", " ")
        line = line.replace(" ", "\t")
        fsave.write(line)
"""
for line in lines:
    if "6A900" in line:
        line = line.replace(" (8) Ext", "")
        line = line.replace(" (7) Ext", "")        
        line = line.replace(" : ", " ")
        line = line.replace(" ", "\t")
        fsave.write(line)

fsave.close()