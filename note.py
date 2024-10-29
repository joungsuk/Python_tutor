
sig0 = [0x05, 0x31, 0x01, 0x03, 0x26, 0x01] #Enter Supplier ECU Mode
sig1 = [0x03, 0x22, 0x72, 0x15]             #Supplier ECU Mode Status Check
sig3 = [0x10, 0xF3, 0x2E, 0x72, 0x17]       #Erase the MAC addresses 1
sig4 = [0x21]                               #Erase the MAC addresses 3
sig5 = [0x22]                               #Erase the MAC addresses 4
sig6 = [0x23]                               #Erase the MAC addresses 5

sendSignal = sig0
data = [255] * 64
data[0:len(sendSignal)] = sendSignal

# print("hex : ", "".join(f"{i:02X} " for i in data0))
# print("hex : ", "".join(f"0x{i:02X} " for i in data0))
# print("hex : ", str.join("", (f"{i:02X} " for i in data0)))
