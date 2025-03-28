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


row_index = channel_num  # 0-based 인덱스로 직접 계산

# 폴더 내 CSV 파일 목록
csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".csv")]

results = []

for csv_file in csv_files:
    # 1) trayID 추출 (파일명 예: ..._TrayID_LHAD000513_...)
    match_tray = re.search(r"_TrayID_(.*?)_", csv_file)
    if match_tray:
        tray_id = match_tray.group(1)
    else:
        tray_id = "Unknown"

    # 2) CSV 읽기
    #    헤더가 없다고 가정 (header=None) → 모든 셀을 df.iloc로 접근
    csv_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(csv_path, header=None)

    # 3) 지정된 row_index(=채널번호)에 대해:
    #    - 31번째 열(1-based=열 인덱스30)에서 "채널 식별값" (ex: "Slot_28(mA)" 등)을 가져옴
    #    - 32~102열(1-based=열 인덱스31:102)에서 실제 전류 데이터(71개) 가져옴
    try:
        channel_id_cell = df.iloc[row_index, 30]      # 채널 이름/번호가 있는 셀
        channel_values = df.iloc[row_index, 31:102]   # 71개 전류 데이터
    except IndexError:
        # 혹시 파일에 해당 행/열이 없으면 건너뜀
        print(f"[경고] {csv_file}에서 (row={row_index}, col=30~101) 추출 불가. 행/열 범위 확인 필요.")
        continue

    # 4) 결과 구성: [trayID, 채널번호(또는 채널ID 셀값), 값1, 값2, ..., 값N]
    row_data = [tray_id, channel_id_cell] + channel_values.tolist()
    results.append(row_data)

# --- 결과를 하나의 DataFrame으로 ---
if not results:
    print("추출된 데이터가 없습니다. (해당 채널 행/열을 읽지 못했을 수 있음)")
else:
    # 최대 길이 (파일마다 데이터 개수가 다를 수도 있으니 맞춤)
    max_len = max(len(r) for r in results) - 2  # trayID, channelID 제외

    # 열 이름: trayID, channelID + data1..dataN
    columns = ["trayID", "channelID"] + [f"Data_{i+1}" for i in range(max_len)]

    # 각 행 길이를 맞추어 None으로 채움
    for r in results:
        diff = (2 + max_len) - len(r)
        if diff > 0:
            r.extend([None]*diff)

    df_result = pd.DataFrame(results, columns=columns)
    df_result.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"완료! 결과가 '{output_csv}'에 저장되었습니다.")
