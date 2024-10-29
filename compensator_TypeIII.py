# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 12:16:21 2018

@author: joungsuk
"""

import numpy as np
from scipy import signal

R1 = 8.42e3
R2 = 265e3
R3 = 889e3
C1 = 390e-12
C2 = 10e-9
C3 = 3.58e-12

num = [C2*C1*R3*R2, (C2*R3 + C1*R2), 1]
den = [-C3*C2*C1*R3*R2*R1, 
       -C3*C2*R3*R1 - C3*C2*R3*R2 - C3*C1*R2*R1 - C2*C1*R2*R1, 
       -C3*R1-C3*R2 - C2*R1 - C2*R2, 
       0]

comp = signal.TransferFunction(num, den)

print("Compensator Transfunction =")
print(comp)
print("\n")


comp_z = comp.zeros
comp_p = comp.poles
print("zeros =")
print(comp_z)
print("\npoles =")
print(comp_p)

print("\nPole-zero frequency (Hz)")

print('fcz1 = %8.2f' % (-comp_z[1] / (2.0 * np.pi)))
print('fcz0 = %8.2f' % (-comp_z[0] / (2.0 * np.pi)))

print('fcp2 = %8.2f' % (-comp_p[2] / (2.0 * np.pi)))
print('fcp1 = %8.2f' % (-comp_p[1] / (2.0 * np.pi)))
print('fcp0 = %8.2f' % (-comp_p[0] / (2.0 * np.pi)))

"""
print('fz1 = %8.2f' % -z[1] * 2.0 * np.pi)
print('fz0 = %8.2f' % -z[0] * 2.0 * np.pi)


print('fp2 = %8.2f', -p[2] * 2 * np.pi)
print('fp1 = %8.2f', -p[1] * 2 * np.pi)
print('fp0 = %8.2f', -p[0] * 2 * np.pi)

"""