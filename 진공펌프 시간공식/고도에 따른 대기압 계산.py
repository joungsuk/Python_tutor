import math

def calculate_atmospheric_pressure(altitude_m):
    """
    고도를 입력받아 기압 공식(Barometric Formula)으로 대기압을 계산합니다.

    Args:
        altitude_m: 해수면으로부터의 고도 (미터)

    Returns:
        대기압 (kPa, atm, mmHg, psia)을 담은 딕셔너리
    """
    P0 = 101325  # 해수면 기준 대기압 (Pa)
    L = 0.0065    # 대기 온도 변화율 (K/m)
    T0 = 288.15   # 해수면 기준 온도 (K)
    g = 9.80665   # 중력 가속도 (m/s^2)
    M = 0.0289644 # 건조 공기 몰 질량 (kg/mol)
    R = 8.31447   # 이상 기체 상수 (J/(mol*K))

    try:
        altitude_m = float(altitude_m)
        if altitude_m < 0:
            return "오류: 고도는 0 이상이어야 합니다."

        term = (1 - (L * altitude_m) / T0)
        if term < 0:
            return "오류: 계산 중 오류가 발생했습니다. 입력 값을 확인해주세요."

        exponent = (g * M) / (R * L)
        pressure_pa = P0 * (term ** exponent)

        pressure_kpa = pressure_pa / 1000
        pressure_atm = pressure_pa / 101325
        pressure_mmhg = pressure_pa * 0.00750061683
        pressure_psia = pressure_pa * 0.000145037738

        return {
            "kPa": pressure_kpa,
            "atm": pressure_atm,
            "mmHg": pressure_mmhg,
            "psia": pressure_psia
        }

    except ValueError:
        return "오류: 유효한 숫자 형태의 고도를 입력해주세요."

if __name__ == "__main__":
    altitude_input = input("고도 (미터)를 입력하세요: ")
    result = calculate_atmospheric_pressure(altitude_input)

    if isinstance(result, str):
        print(result)
    else:
        print("\n고도에 따른 대기압:")
        print(f"  기압 (kPa): {result['kPa']:.4f}")
        print(f"  기압 (atm): {result['atm']:.4f}")
        print(f"  기압 (mmHg): {result['mmHg']:.4f}")
        print(f"  기압 (psia): {result['psia']:.4f}")