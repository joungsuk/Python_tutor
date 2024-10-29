# -*- coding: utf-8 -*-
"""
Created on Thu May 24 13:06:01 2018

@author: joungsuk
"""

import pandas as pd
import math
from scipy import signal

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

def window_average(data, w_size):
    y = []
    for idx in np.arange(w_size, len(data) + 1, w_size):
        y.append((sum(data[idx-w_size:idx])/w_size))
    
    y = np.asarray(y)
    return y

aaa = np.full(1000, 100)

bbb = window_average(aaa, 200)
print(bbb)