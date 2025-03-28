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

row_index = channel_num     # CSV에서 channel_num+1(1-based) 행에 데이터가 있다고 가정(헤더 없을 때)

# (예) 전류 데이터가 71개라면, 가령 열 31~102(1-based) → 파이썬에선 30~101(0-based)
col_channel_id = 30         # 채널 식별자("Slot_28(mA)" 등) 위치
col_data_start = 31         # 전류 데이터 시작 열
col_data_end   = 102        # 전류 데이터 끝(슬라이싱에서 제외될 인덱스)

# 폴더 내 CSV 파일 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".csv")]

# 추출 결과 누적용 리스트
# (이후 DataFrame으로 만들 때: [trayID, channelID, Data_1, Data_2, ..., Data_71])
results = []

for csv_file in csv_files:
    csv_path = os.path.join(folder_path, csv_file)

    # 1) 파일명에서 trayID 추출
    #    예: "..._TrayID_LHAD001221_..."
    match_tray = re.search(r"_TrayID_(.*?)_", csv_file)
    if match_tray:
        tray_id = match_tray.group(1)
    else:
        tray_id = "Unknown"

    # 2) CSV 읽기 (헤더가 없다고 가정)
    #    필요하다면 skiprows, sep 등을 조정
    df = pd.read_csv(csv_path, header=None)

    # 3) 해당 row_index 행에서 channelID, 전류데이터(71개) 추출
    try:
        channel_id_cell = df.iloc[row_index, col_channel_id]         # e.g. "Slot_28(mA)"
        channel_values = df.iloc[row_index, col_data_start:col_data_end].tolist()
    except IndexError:
        print(f"[경고] '{csv_file}'에서 (row={row_index}, col={col_channel_id}~{col_data_end-1}) 추출 불가.")
        continue

    # 4) 한 행: [trayID, channelID, data1, data2, ..., dataN]
    row_data = [tray_id, channel_id_cell] + channel_values
    results.append(row_data)

# --- 모든 파일 처리 후, DataFrame 구성 ---
if not results:
    print("추출된 데이터가 없습니다.")
else:
    # 채널 데이터 최대 개수 확인
    # (혹시 파일마다 샘플 수가 다를 수 있으니 길이 맞춤)
    max_len = max(len(r) for r in results) - 2  # trayID, channelID 제외
    
    # 컬럼 명: [trayID, channelID, Data_1..Data_N]
    columns = ["trayID", "channelID"] + [f"Data_{i+1}" for i in range(max_len)]
    
    # 행마다 부족한 부분 None으로 채우기
    for r in results:
        diff = (2 + max_len) - len(r)
        if diff > 0:
            r.extend([None]*diff)
    
    df_all = pd.DataFrame(results, columns=columns)

    # 1) channelID 열 제거
    df_all = df_all.drop(columns=["channelID"])

    # 2) trayID를 인덱스로 설정 → transpose
    #    (원래 Data_1..Data_n 컬럼이 행이 되고, trayID가 열이 됨)
    df_pivot = df_all.set_index("trayID").T

    # 3) CSV로 저장: 인덱스(=Data_1..Data_n) 안 쓰고, 헤더(=trayID)는 표시
    df_pivot.to_csv(output_csv, index=False, header=True, encoding="utf-8-sig")

    print(f"완료! 결과 CSV: {output_csv}")
