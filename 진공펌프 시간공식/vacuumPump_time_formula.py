import math

# 상수 정의
atmospheric_pressure_kPa = 101.325  # kPa (표준 대기압)
atmospheric_pressure_Pa = atmospheric_pressure_kPa * 1000  # Pa

def calculate_vacuum_time(chamber_volume, pump_capacity, target_pressure_kPa):
    """
    챔버 내 목표 진공 압력에 도달하는 시간을 계산합니다.
    
    :param chamber_volume: 챔버의 체적 (리터, L)
    :param pump_capacity: 진공 펌프의 용량 (리터/초, L/s)
    :param target_pressure_kPa: 목표 진공 압력 (킬로파스칼, kPa), 양수 또는 음수 가능
    :return: 목표 압력에 도달하는 시간 (초, s)
    """
    
    # 목표 압력을 kPa에서 절대 압력 Pa로 변환
    if target_pressure_kPa < 0:
        absolute_target_pressure_Pa = atmospheric_pressure_Pa + target_pressure_kPa * 1000
    else:
        absolute_target_pressure_Pa = target_pressure_kPa * 1000
    
    # 목표 압력이 유효한지 확인
    if absolute_target_pressure_Pa >= atmospheric_pressure_Pa or absolute_target_pressure_Pa <= 0:
        raise ValueError("목표 압력은 대기압보다 낮고 0보다 커야 합니다.")
    
    # 로그 감쇠식을 사용하여 진공 펌프의 시간을 계산
    time = (chamber_volume / pump_capacity) * math.log(atmospheric_pressure_Pa / absolute_target_pressure_Pa)
    
    return time

# 예제 입력 값
try:
    chamber_volume_input = float(input("챔버의 체적을 입력하세요 (리터, L): "))
    pump_capacity_input = float(input("진공 펌프의 용량을 입력하세요 (리터/초, L/s): "))
    target_pressure_input = float(input("목표 진공 압력을 입력하세요 (킬로파스칼, kPa, 양수 또는 음수 가능): "))

    # 진공 시간 계산
    vacuum_time = calculate_vacuum_time(chamber_volume_input, pump_capacity_input, target_pressure_input)
        
    # 결과 출력
    print(f"목표 진공 압력에 도달하는 시간: {vacuum_time:.2f}초 ({vacuum_time / 60:.2f}분)")

except ValueError as ve:
    print(f"입력 오류: {ve}")