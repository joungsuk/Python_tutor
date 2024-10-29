# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 12:48:02 2018

@author: joungsuk
"""

Kp = 0.1
Ki = 0.001
rkV = 0.6
fbdV = 0.7
fbdI = -0.25

i6 = 1
i10 = 0.0
Umax = 0.0
Umin = -0.2

Ii6 = 1
Ii10 = 0.25
IUmax = 0.5
IUmin = 0.05

for i in range(1,100):
    v1 = rkV - fbdV
    v2 = Kp * v1
    v4 = (v1 * Ki) * i6 + i10
    i10 = v4
    v5 = v2 + v4
    v9 = Umax if (v5 > Umax) else v5
    v9 = Umin if (v9 < Umin) else v9
    i6 = (v5 == v9) if 1 else 0
    
    Iv1 = v9 - fbdI
    Iv2 = Kp * Iv1
    Iv4 = (Iv1 * Ki) * Ii6 + Ii10
    Ii10 = Iv4
    Iv5 = Iv2 + Iv4
    Iv9 = IUmax if (Iv5 > IUmax) else Iv5
    Iv9 = IUmin if (Iv9 < IUmin) else Iv9
    Ii6 = (Iv5 == Iv9) if 1 else 0
    print(i, v9, Iv9, Ii10)
