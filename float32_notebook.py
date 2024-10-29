
10# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 19:40:31 2019

@author: jslee
"""

import numpy as np

max_v = 6250
max_i = 61750
max_p = max_v * max_i


max_v = 6250
max_i = 61750
max_p = max_v * max_i

norm_v = 1/max_v
norm_i = 1/max_i
norm_p = 1/max_p

targetV = 4200
targetI = 5000
"""
rv = targetV * norm_v
ri = targetI * norm_i

targetP = targetV * targetI

rp = rv * ri

print("error = %1.25f\n" % (targetP - rp / norm_p))
"""

fnorm_v = np.float32(1/max_v)
fnorm_i = np.float32(1/max_i)
fnorm_p = np.float32(1/max_p)

"""
ftargetV = np.float32(4000)
ftargetI = np.float32(50000)

frealV = np.float32(4100)
frrv = frealV * fnorm_v

frv = ftargetV * fnorm_v
fri = ftargetI * fnorm_i

ftargetP = ftargetV * ftargetI
frp = frv * fri

frri = frp / frrv
print("error = %1.25f\n" % (frp - frrv * frri))

"""

fnv = np.float32(1/max_v)
fni = np.float32(1/max_i)
fnp = np.float32(1/max_p)

power = np.float32(4000)
v = np.float32(5000)
i = power / v * np.float32(1000)
print('current = %f' %(i))
tgp = np.float32(v * fnv) * np.float32(i * fni)

vr = np.float32(3700) * fnv
ir = tgp / vr

pr = vr * ir



"""
code_max = np.float32(65535)
ref_volt = np.float32(2500)
gain = np.float32(101.2*0.8)
shunt = np.float32(0.0005)

a0 = 65535.0 /( 2500.0 / (101.2*0.8) / 0.0005)
a1 = code_max / (ref_volt / gain / shunt)
a2 = code_max / (ref_volt / ( gain * shunt))
"""

