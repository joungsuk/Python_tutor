# -*- coding: utf-8 -*-
"""
Created on Wed May 23 19:09:53 2018

@author: joungsuk
"""
import pandas as pd
import math
from scipy import signal

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


raw_data = pd.read_csv('data2.csv', header=None)

raw_data = raw_data.values #dataframe to ndarray

raw_data = raw_data - sum(raw_data)/len(raw_data)

raw_data = raw_data / 2**17 * 50

# Filter requirements.
order = 2
fs = 10000       # sample rate, Hz
cutoff = 1000  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=8000)
plt.subplot(4, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


# Demonstrate the use of the filter.
# First make some data to be filtered.
#T = 0.01         # seconds
T = 1/fs * len(raw_data)
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 5kHz signal from this.
data = np.sin(1000*2*np.pi*t) + 0.5*np.cos(10000*2*np.pi*t) + 1.5*np.sin(25000.0*2*np.pi*t)

# Filter the data, and plot both the original and filtered signals.
#y = butter_lowpass_filter(data, cutoff, fs, order)
y = butter_lowpass_filter(raw_data, cutoff, fs, order)

y2 = butter_lowpass_filter(y, cutoff, fs, order)

xrange = 0.05

plt.subplot(4, 1, 2)
plt.plot(t, raw_data, 'b-')
plt.xlabel('Time [sec]')
plt.xlim( 0, xrange)
plt.grid()

plt.subplot(4, 1, 3)
plt.plot(t, y, 'g-', linewidth=2)
plt.xlabel('Time [sec]')
plt.xlim( 0, xrange)
plt.grid()

plt.subplot(4, 1, 4)
plt.plot(t, y2, 'r-', linewidth=2)
plt.xlabel('Time [sec]')
plt.xlim( 0, xrange)
plt.grid()

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