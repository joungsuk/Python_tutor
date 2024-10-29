# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 09:36:04 2021

@author: jslee
"""
import warnings
#with warnings.catch_warnings():
warnings.filterwarnings("ignore",category=FutureWarning)

from fxpmath import Fxp



TEMP_CAL = Fxp(1.2, False, 22, 11)
msg1 = 'TEMP_CAL = {}'.format(TEMP_CAL.hex())
print(msg1)

TEMP_CAL = Fxp(1.4, False, 22, 11)
msg1 = 'TEMP_CAL = {}'.format(TEMP_CAL.hex())
print(msg1)

TEMP_CAL = Fxp(1.6, False, 22, 11)
msg1 = 'TEMP_CAL = {}'.format(TEMP_CAL.hex())
print(msg1)
print("")



CURRENT_GAIN_T0 = Fxp(1.0, True, 16, 14)
msg1 = 'CURRENT_GAIN_T0 = {}'.format(CURRENT_GAIN_T0.hex())
print(msg1)
CURRENT_GAIN_T0 = Fxp(0.9, True, 16, 14)
msg1 = 'CURRENT_GAIN_T0 = {}'.format(CURRENT_GAIN_T0.hex())
print(msg1)

print("")

#I_PID_KP = Fxp(0.1, True, 28, 20)
I_PID_KP = Fxp(0.5, True, 28, 20)
msg1 = 'I_PID_KP = {}'.format(I_PID_KP.hex())
print(msg1)

#I_PID_KI = Fxp(0.004, True, 28, 20)
I_PID_KI = Fxp(0.25, True, 28, 20)
msg1 = 'I_PID_KI = {}'.format(I_PID_KI.hex())
print(msg1)

I_PID_KD = Fxp(0.00, True, 28, 20)
msg1 = 'I_PID_KD = {}'.format(I_PID_KD.hex())
print(msg1)

print("")

V_PID_KP = Fxp(0.5, True, 28, 20)
msg1 = 'V_PID_KP = {}'.format(V_PID_KP.hex())
print(msg1)

V_PID_KI = Fxp(0.025, True, 28, 20)
msg1 = 'V_PID_KI = {}'.format(V_PID_KI.hex())
print(msg1)


V_PID_KD = Fxp(0.00, True, 28, 20)
msg1 = 'V_PID_KD = {}'.format(V_PID_KD.hex())
print(msg1)

print("")



vhi_thld = Fxp(-0.006/5, True, 16, 15)
msg1 = 'vhi_thld = {}'.format(vhi_thld.hex())
print(msg1)

vlow_thld = Fxp(-0.1/5, True, 16, 15)
#value = vlow_thld.hex()
#msg1 = f'vlow_thld = {value}'
msg1 = 'vlow_thld = {}'.format(vlow_thld.hex())
print(msg1)

print("")

ihi_thld = Fxp(0/62.5, True, 16, 15)
msg1 = 'ilhi_thld = {}'.format(ihi_thld.hex())
print(msg1)

ilow_thld = Fxp(-52.5/62.5, True, 16, 15)
msg1 = 'ilow_thld = {}'.format(ilow_thld.hex())
print(msg1)

print("")

vref = Fxp(3.6/5, False, 15, 15)
msg1 = 'vref = {}'.format(vref.hex())
print(msg1)

iref = Fxp(62.5/62.5, False, 15, 15)
msg1 = 'iref = {}'.format(iref.hex())
print(msg1)

