def crc16_ccitt(data: bytes, poly: int = 0x1021, init_val: int = 0xFFFF) -> int:
    crc = init_val
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF  # 16비트 마스킹
    return crc

# 예제 문자열
input_data = "123456789".encode()
crc_result = crc16_ccitt(input_data)
print(f"CRC16-CCITT: {crc_result:04X}")
