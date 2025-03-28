import os
import re
import pandas as pd
import logging
from datetime import datetime

# 설정값
CURRENT = True
LOGGING_ENABLED = False  # 로깅 on/off 플래그

# 로깅 설정
if LOGGING_ENABLED:
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
        
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_folder, f'data_extract_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'))
        ]
    )
else:
    # 로깅 비활성화
    logging.getLogger().setLevel(logging.CRITICAL)

# config.py 파일 생성 추천

# 기본 설정 (전류 데이터)
if CURRENT:
    col_channel_id = 30     # 31번째 열 (0-based index)
    col_data_start = 31     # 32번째 열 (0-based index)
    col_data_end = 103      # 102번째 열까지 포함 (0-based index, exclusive)
else:
    col_channel_id = 103    # 104번째 열
    col_data_start = 104    # 105번째 열
    col_data_end = 175      # 174번째 열까지 포함 (0-based index, exclusive)

if LOGGING_ENABLED:
    logging.info(f"현재 설정: CURRENT={CURRENT}")
    logging.info(f"열 범위: channel_id={col_channel_id}, start={col_data_start}, end={col_data_end}")

CONFIG = {
    'folder_path': r"D:\tmp\hpcd_0326",
    'col_channel_id': col_channel_id,
    'col_data_start': col_data_start,
    'col_data_end': col_data_end,
    'channels_range': range(1, 37)
}

# --- 사용자가 지정할 부분 ---
folder_path = CONFIG['folder_path']   # CSV들이 모여있는 폴더 경로
ext_folder = os.path.join(folder_path, "output")  # 결과 저장용 "ext" 폴더 경로

# CSV 구조 관련 설정: (아래 예시는, 1번 채널 -> 2행, 28번 채널 -> 29행)
# => row_index = channel_num
col_channel_id = CONFIG['col_channel_id']         # 채널 식별자(예: "Slot_28(mA)" 등)가 적힌 열 (0-based)
col_data_start = CONFIG['col_data_start']         # 전류 데이터 시작 열 인덱스 (0-based)
col_data_end   = CONFIG['col_data_end']        # 전류 데이터 끝(슬라이싱) 인덱스 (파이썬에서는 제외 인덱스)

# 폴더 내 CSV 파일 모으기
csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".csv")]

# 결과를 저장할 하위 폴더 'ext'가 없으면 생성
if not os.path.exists(ext_folder):
    os.makedirs(ext_folder)

# --- 1) 1~36 채널을 순회 ---
for channel_num in CONFIG['channels_range']:
    row_index = channel_num  # N번 채널 -> CSV상 N+1행(1-based), pandas에선 row_index=N
    
    # 채널별 결과를 담을 임시 리스트
    results = []
    
    # 2) 폴더 내 모든 CSV 파일 처리
    for csv_file in csv_files:
        try:
            csv_path = os.path.join(folder_path, csv_file)
            
            if not os.path.exists(csv_path):
                logging.error(f"파일을 찾을 수 없음: {csv_path}")
                continue
            
            # trayID 추출 (파일명 예: "..._TrayID_LHAD000680_...")
            match_tray = re.search(r"_TrayID_(.*?)_", csv_file)
            if not match_tray:
                logging.warning(f"TrayID를 찾을 수 없음: {csv_file}")
                tray_id = "Unknown"
            else:
                tray_id = match_tray.group(1)

            # CSV 읽기 전에 파일 정보 확인
            try:
                # 먼저 전체 열 수를 확인
                df_test = pd.read_csv(csv_path, header=None, nrows=1)
                logging.info(f"CSV 파일의 전체 열 수: {len(df_test.columns)}")
                
                df = pd.read_csv(csv_path, header=None, usecols=range(col_channel_id, col_data_end))
                logging.info(f"데이터프레임 크기: {df.shape}")
                logging.info(f"사용된 열: {list(df.columns)}")
            except Exception as e:
                logging.error(f"CSV 읽기 오류: {str(e)}")
                continue
            
            # 시간 데이터 추출 (첫 번째 행)
            time_values = df.iloc[0, 1:].values.tolist()
            
            # row_index 행에서 channel 식별자, 전류값 추출
            try:
                channel_id_cell = df.iloc[row_index, 0]  # 예: "Slot_28(mA)"
                channel_values = df.iloc[row_index, 1:].values.tolist()
            except IndexError:
                print(f"[경고] {csv_file}에서 (row={row_index}, col={col_data_start}~{col_data_end-1}) 범위 추출 실패.")
                continue

            # 필요한 데이터만 메모리에 로드 (시간 데이터 포함)
            row_data = [tray_id, channel_id_cell] + channel_values
            if len(results) == 0:  # 첫 번째 파일인 경우에만 시간 데이터 추가
                time_row = ["Time", "Time"] + time_values
                results.append(time_row)
            results.append(row_data)
            
            # 메모리에서 즉시 해제
            del df

        except Exception as e:
            logging.error(f"파일 처리 중 오류 발생 ({csv_file}): {str(e)}")
            continue

    # --- 3) 해당 채널에 대한 모든 파일 처리 후, DataFrame으로 생성 ---
    if not results:
        print(f"채널 {channel_num} 추출 결과가 없습니다.")
        continue
    
    # 최대 전류 데이터 길이 파악 (시간 데이터 행 포함)
    max_len = max(len(r) for r in results) - 2  # trayID, channelID 제외
    columns = ["trayID", "channelID"] + [f"Data_{i+1}" for i in range(max_len)]

    # 길이 부족한 행을 None으로 채움
    for r in results:
        diff = (2 + max_len) - len(r)
        if diff > 0:
            r.extend([None]*diff)
    
    df_all = pd.DataFrame(results, columns=columns)
    
    # 4) channelID 열 제거
    df_all = df_all.drop(columns=["channelID"])

    # 5) trayID를 인덱스로 설정 -> 전치(Transpose)
    #    => 각 trayID가 열, 기존 Data_1..Data_n 가 행
    df_pivot = df_all.set_index("trayID").T

    # 6) CSV 저장
    #    예: "전류데이터_Ch01.csv" 또는 "전압데이터_Ch01.csv"
    suffix = "전류데이터" if CURRENT else "전압데이터"
    output_csv = os.path.join(ext_folder, f"Ch{channel_num:02d}_{suffix}.csv")

    #   - index=False → 인덱스(Data_1 등) 안쓰도록
    #   - header=True  → trayID가 맨 윗줄에 들어감
    df_pivot.to_csv(output_csv, index=False, header=True, encoding="utf-8-sig", sep=",")
    
    print(f"채널 {channel_num} 추출 완료 -> {output_csv}")
