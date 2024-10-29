# -*- coding: utf-8 -*-
"""
Created on Wed May 23 17:35:36 2018

@author: joungsuk
"""

import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import math

"""
file = open('data.csv', 'r')
rdr = csv.reader(file)

n = []

for line in rdr:
    n.append(line[0]) #print(line)
    
    
file.close()

a = n
"""
raw_data = pd.read_csv('data2.csv', header=None)

y = raw_data.values #dataframe to ndarray

#y = y - sum(y)/len(y)

Fs = 100000
T = 1/Fs
te = T * len(y)
t = np.arange(0, te, T)


y2 = [y[0]]
samplesize = 8
for idx in np.arange(samplesize, len(y), samplesize):
    y2.append((sum(y[idx-(samplesize):idx])/samplesize))


y2e = [y[0]]
multiplier = 2 * np.pi * 3000 / 100000
for idx in np.arange(1, len(y), 1):
    y2e.append((y[idx] - y2e[idx-1]) * multiplier + y2e[idx-1])

"""    
y3 = []
samplesize = 20
for idx in np.arange(samplesize - 1, len(y2), samplesize):
    y3.append((sum(y2[idx-(samplesize-1):idx])/samplesize))
"""

y2 = np.asarray(y2)
y2e = np.asarray(y2e)
#y3 = np.asarray(y3)

y = y / 2**17 * 50
y2 = y2 / 2**17 * 50
y2e = y2e / 2**17 * 50
#y3 = y3 / 2**17 * 50


print("min y =", min(y), "     max y =", max(y))
print("delta y =", max(y) - min(y))

print("min y2 =", min(y2), "     max y2 =", max(y2))
print("delta y2 =", max(y2) - min(y2))

print("min y2e =", min(y2e), "     max y2e =", max(y2e))
print("delta y2e =", max(y2e) - min(y2e))


#print("min y3 =", min(y3), "     max y3 =", max(y3))
#print("delta y3 =", max(y3) - min(y3))


"""
# Sum of a 50 Hz sinusoid and a 120 Hz sinusoid
#noise = np.random.normal(0,0.05,len(t))
x = 0.6*np.cos(2*np.pi*60*t+np.pi/2) + np.cos(2*np.pi*120*t)
y = x  # + noise     # Sinusoids plus noise
#y = raw_data.values #dataframe to ndarray

plt.figure(num=1,dpi=100,facecolor='white')
plt.plot(t,y,'r')
plt.xlim(0, te)
plt.xlabel('time($sec$)')
plt.ylabel('y')
plt.savefig("./test_figure1.png",dpi=300)


# Calculate FFT ....................
n=len(y)        # Length of signal
NFFT=n      # ?? NFFT=2^nextpow2(length(y))  ??
k=np.arange(NFFT)
f0=k*Fs/NFFT    # double sides frequency range
f0=f0[range(math.trunc(NFFT/2))]        # single side frequency range

Y=np.fft.fft(y)/NFFT        # fft computing and normaliation
Y=Y[range(math.trunc(NFFT/2))]          # single side frequency range
amplitude_Hz = 2*abs(Y)
phase_ang = np.angle(Y)*180/np.pi
"""
# figure 1 ..................................
xrange = 2500

plt.figure(num=2,dpi=100,facecolor='white')
plt.subplots_adjust(hspace = 0.5, wspace = 0.3)
plt.subplot(3,1,1)

plt.plot(y,'r')
plt.xlim( 0, xrange)
#plt.title('Signal FFT analysis')
#plt.xlabel('time($sec$)')
#plt.ylabel('y')
#plt.xlim( 0, 0.1)
plt.grid()

# Amplitude ....
#plt.figure(num=2,dpi=100,facecolor='white')
plt.subplot(3,1,2)

# Plot single-sided amplitude spectrum.

plt.plot(y2,'r')   #  2* ???
plt.xlim( 0, xrange/samplesize)
#plt.xticks(np.arange(0,500,20))
#plt.xlim( 0, 5000)
#plt.ylim( 0, 1.2)
#plt.title('Single-Sided Amplitude Spectrum of y(t)')
#plt.xlabel('frequency($Hz$)')
#plt.ylabel('amplitude')
plt.grid()

# Phase ....
#plt.figure(num=2,dpi=100,facecolor='white')
plt.subplot(3,1,3)
plt.plot(y2e,'r')   #  2* ???
plt.xlim( 0, xrange)
#plt.xlim( 0, 200)
#plt.ylim( -180, 180)
#plt.title('Single-Sided Phase Spectrum of y(t)')
#plt.xlabel('frequency($Hz$)')
#plt.ylabel('phase($deg.$)')
#plt.xticks([0, 60, 120, 200])
#plt.yticks([-180, -90, 0, 90, 180])
plt.grid()

#plt.savefig("./test_figure2.png",dpi=300)
plt.show()
