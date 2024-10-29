# -*- coding: utf-8 -*-
"""
Created on Wed May 23 19:09:53 2018

@author: joungsuk
"""
import pandas as pd
#import math
import numpy as np
#from scipy import signal
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def ema_filter(data, cutoff, fs):
    multiplier = 2 * np.pi * cutoff / fs
    y = [data[0]]
    for idx in np.arange(1, len(data-1), 1):
        y.append((data[idx] - y[idx-1]) * multiplier + y[idx-1])
        
    y = np.asarray(y)
    return y


def print_statics(data):
    Dmin = min(data)
    Dmax = max(data)
    Ddiff = Dmax - Dmin
    print('min = ', Dmin, ' max = ', Dmax, ' delta = ', Ddiff)
    return


def window_average(data, w_size):
    y = []
    for idx in np.arange(w_size, len(data) + 1, w_size):
        y.append((sum(data[idx-w_size:idx])/w_size))
    
    y = np.asarray(y)
    return y

import_data = pd.read_csv('data2.csv', header=None)
raw_data = np.asarray(import_data[0].tolist())
raw_data = raw_data - raw_data.mean()
raw_data = raw_data * 50 / (2**17)

'''
raw_data = np.full(150*100, 1)
raw_data[0:500] = 0
'''


# Filter requirements.
order = 2
fs = 100000       # sample rate, Hz
cutoff = 1000  # desired cutoff frequency of the filter, Hz

fs2 = 1000
cutoff2 = 50

w1 = 100
w2 = 20


# Demonstrate the use of the filter.
# First make some data to be filtered.
#T = 0.01         # seconds
T = 1/fs * len(raw_data)
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 5kHz signal from this.
#data = np.sin(1000*2*np.pi*t) + 0.5*np.cos(10000*2*np.pi*t) + 1.5*np.sin(25000.0*2*np.pi*t)

# Filter the data, and plot both the original and filtered signals.
#y = butter_lowpass_filter(data, cutoff, fs, order)

ema_result = ema_filter(raw_data, 10000, fs)
y1 = butter_lowpass_filter(raw_data, cutoff, fs, order)
y1avg = window_average(y1, w1)
y2 = butter_lowpass_filter(y1avg, cutoff2, fs2, order)
#y2avg = window_average(y2, w2)
y2avg = ema_filter(y2, 20, fs2)

print('\n raw data')
print_statics(raw_data)
print('\n ema_result')
print_statics(ema_result)
print('\n 1st iir')
print_statics(y1)
print('\n 1msec avg 1st iir')
print_statics(y1avg)
print('\n 2nd iir')
print_statics(y2)
print('\n 20msec avg 2nd iir')
print_statics(y2avg)


# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
plot_cnt = 7
w, h = freqz(b, a, worN=8000)
plt.figure(figsize=(14,20))
plt.subplot(plot_cnt, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


xrange = 0.3

plt.subplot(plot_cnt, 1, 2)
plt.plot(t, raw_data, 'b-', label='raw')
plt.xlabel('Time [sec]')
#plt.xlim( 0, xrange)
plt.grid()
plt.legend()

plt.subplot(plot_cnt, 1, 3)
plt.plot(t, y1, 'g-', linewidth=2, label='1st')
plt.xlabel('Time [sec]')
#plt.xlim( 0, xrange)
plt.grid()
plt.legend()

plt.subplot(plot_cnt, 1, 4)
plt.plot(y1avg, 'r-', linewidth=2, label='1ms avg')
plt.xlabel('Time [msec]')
#plt.xlim( 0, xrange/w1)
plt.grid()
plt.legend()

plt.subplot(plot_cnt, 1, 5)
plt.plot(y2, 'r-', linewidth=2, label='2nd')
plt.xlabel('Time [msec]')
#plt.xlim( 0, xrange)
plt.grid()
plt.legend()

plt.subplot(plot_cnt, 1, 6)
plt.plot(y2avg, 'r-', linewidth=2, label='20ms avg')
#plt.xlabel('Time [sec]')
#plt.xlim( 0, xrange/w1/w2)
plt.grid()
plt.legend()

plt.subplot(plot_cnt, 1, 7)
plt.plot(ema_result, 'r-', linewidth=2, label='ema')
plt.xlabel('Time [sec]')
#plt.xlim( 0, xrange/w1/w2)
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()


"""
# Original source code - 2018-05-24
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Filter requirements.
order = 6
fs = 30.0       # sample rate, Hz
cutoff = 3.667  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


# Demonstrate the use of the filter.
# First make some data to be filtered.
T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 1.2 Hz signal from this.
data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()
"""