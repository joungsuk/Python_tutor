# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 15:17:40 2019

@author: joungsuk
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

sample_freq = 20
cutoff_freq = 0.3

ema_in = 0.0
ema_out = 0.0
ema_mult = 2 * np.pi * cutoff_freq / sample_freq

print(ema_mult)

ref = 2000

length = 200

t = np.zeros(length)
y = np.zeros(length)

for x in range(1, length):
    ema_in = ref
    if (x == 100):
        ema_in = 2200
    #ema_out = (ema_in - ema_out) * ema_mult + ema_out
    ema_out = (ema_mult * ema_in) + ((1-ema_mult) * ema_out)
    print("%d, %f" % (x, ema_out))
    t[x] = x
    y[x] = ema_out
    
plt.plot(t,y)
    
