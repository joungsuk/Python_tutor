# -*- coding: utf-8 -*-
"""
Created on Wed May  2 10:17:02 2018

@author: joungsuk
"""

rkWeight = 500;

rkI = 0.5
fdb = 0.0
i10 = 0.2
test_Ki = 0.0003

for i in range(1,500):
    if (rkWeight):
        rkWeight -= 1
        
#        if ((rkI * 0.9) > fdb):
#            i10 += test_Ki
#            fdb += 0.02
#        elif ((rkI * 0.9) < fdb):
#            i10 -= test_Ki
#            fdb -= 0.02
#        else:
#            rkWeight = 0
        
        if (rkI > 0):
            if ((rkI * 0.9) > fdb):
                i10 += test_Ki
            elif (rkI < fdb):
                i10 -= test_Ki
            fdb += 0.02
        else:
            if ((rkI * 0.9) < fdb):
                i10 -= test_Ki
            elif (rkI > fdb):
                i10 += test_Ki
            fdb -= 0.02
            
        print(rkWeight, rkI, fdb, i10)
    

