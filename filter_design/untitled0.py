# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 18:49:14 2018

@author: joungsuk
"""

import visa

rm = visa.ResourceManager()
rm.list_resources()

dmm = rm.open_resource('USB0::0x0957::0x0607::MY47031648::INSTR')

print(dmm.query('*IDN?'))

dmm.write('SAMP:COUN 1')        #1회 트리거시 샘플링 갯 수 지정, 34410A는 50000까지 가능

dmm.write('TRIG:COUN 100')      #트리거 횟수 지정, 별도 소스 지정이 없었으므로 인터널 트리거

dmm.write('INIT')               #측정 시작

dmm.query('DATA:POIN?')         #내부 메모리에 캡쳐된 데이터 갯수 확인, 측정 중에 쿼리도 가능.
                                #DATA:POINts? [{RDG_STORE|NVMEM}]

dmm.query('FETC?')              #측정 데이터 전체를 리딩, 내부 메모리에 데이터는 그대로 남아 있음.

dmm.query('DATA:DATA? NVMEM')   #This command returns all readings in non-volatle memory, 
                                #INIT로 측정한 값이 저장되는 공간은 별도로 있음.(NVMEM이 아님.)
                                
dmm.query('DATA:REMove? 3')     #This command reads and erases the specified number of readings from memory.