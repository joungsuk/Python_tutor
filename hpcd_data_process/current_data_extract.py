import os
import re
import pandas as pd

# --- 사용자가 지정할 부분 ---
folder_path = r"D:\usr\python\hpcd_data_process\raw"   # CSV들이 모여있는 폴더 경로
output_csv = r"D:\usr\python\hpcd_data_process\raw통합_채널추출.csv"

# (A) 사용자 입력: 추출할 채널 번호
channel_num = 28  # 2번 채널을 예로 듦
# (B) CSV 열(header)과 실제 채널 번호가 매칭되는 방식
#     예: 'Slot_01(mA)', 'Slot_02(mA)' ... 'Slot_36(mA)'
channel_name = f"_{channel_num:02d}"
# (channel_num:02d → 1이면 '01', 2이면 '02' 형태로)

output_csv = rf"D:\usr\python\hpcd_data_process\raw\통합_채널추출_Ch{channel_num}.csv"


# 폴더 내 CSV 파일
csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".csv")]

result_rows = []

for csv_file in csv_files:
    # 1) 파일 경로
    csv_path = os.path.join(folder_path, csv_file)
    
    # 2) trayID 추출 (파일명에서 '_TrayID_' 뒤의 '_' 전까지)
    #    예: "..._TrayID_LHAD000513_Auto.csv" -> "LHAD000513"
    match_tray = re.search(r"_TrayID_(.*?)_", csv_file)
    if match_tray:
        tray_id = match_tray.group(1)
    else:
        tray_id = "Unknown"

    # 3) CSV 읽기 (헤더가 없다고 가정 → header=None)
    #    모든 셀을 숫자/문자 그대로 DataFrame에 불러옴
    df = pd.read_csv(csv_path, header=None)

    # 4) 원하는 행/열에서 데이터 추출
    #  - '채널 번호'가 2행 31번째 열(1-based) → iloc[1, 30]
    #  - '전류 값들'이 2행 32~102열(1-based) → iloc[1, 31:102]
    #    (파이썬은 0-based이므로, 2행=iloc[1], 31번째 열=iloc[...,30])
    try:
        channel_id_cell = df.iloc[channel_num, 30]  # 채널 번호가 기록된 셀
        channel_values = df.iloc[channel_num, 31:102].tolist()  # 전류 데이터 71개 가정
    except IndexError:
        # 혹시 파일에 행/열이 모자라면 건너뜀
        print(f"[경고] {csv_file}에서 지정된 행/열 범위를 읽을 수 없습니다.")
        continue

    # 5) 결과 한 행(row)로 구성: [trayID, 채널번호, 값1, 값2, ..., 값N]
    row_data = [tray_id, channel_id_cell] + channel_values
    result_rows.append(row_data)

# --- 모든 파일 처리 후, 최종 DataFrame ---
if not result_rows:
    print("추출된 데이터가 없습니다. (행/열 범위가 맞지 않거나 폴더가 비었을 수 있음)")
else:
    # 최대 길이(채널 데이터 수) 파악
    # (파일마다 길이 다를 수 있으니 맞춰준다)
    max_len = max(len(r) for r in result_rows) - 2  # tray_id, channel_id_cell 제외

    # 컬럼 이름 지정
    columns = ["trayID", "channelID"] + [f"Data_{i+1}" for i in range(max_len)]

    # 부족한 부분 None(또는 "")으로 채워주기
    for r in result_rows:
        diff = (2 + max_len) - len(r)
        if diff > 0:
            r.extend([None]*diff)

    df_result = pd.DataFrame(result_rows, columns=columns)

    # CSV 저장
    df_result.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"결과 CSV 저장 완료: {output_csv}")
