import os
import re
import csv
import sys

# 실행 파일 경로 설정
if getattr(sys, 'frozen', False):
    # PyInstaller로 생성된 실행 파일로 실행될 때
    application_path = os.path.dirname(sys.executable)
else:
    # 일반 Python 스크립트로 실행될 때
    application_path = os.path.dirname(os.path.abspath(__file__))

# 전류/전압 데이터 설정
DATA_CONFIG = {
    'current': {
        'col_channel_id': 30,    # 31번째 열 (0-based index)
        'col_data_start': 31,    # 32번째 열 (0-based index)
        'col_data_end': 103,     # 102번째 열까지 포함 (0-based index, exclusive)
        'name': '전류데이터'
    },
    'voltage': {
        'col_channel_id': 103,   # 104번째 열
        'col_data_start': 104,   # 105번째 열
        'col_data_end': 175,     # 174번째 열까지 포함 (0-based index, exclusive)
        'name': '전압데이터'
    }
}

BASE_CONFIG = {
    'folder_path': application_path,  # 실행 파일이 있는 폴더로 설정
    'channels_range': range(1, 37)
}

def read_csv_columns(file_path, start_col, end_col):
    data = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row:  # 빈 행 건너뛰기
                data.append(row[start_col:end_col])
    return data

def extract_data(data_type, config):
    folder_path = BASE_CONFIG['folder_path']
    ext_folder = os.path.join(folder_path, "output")
    
    if not os.path.exists(ext_folder):
        os.makedirs(ext_folder)
    
    # CSV 파일 목록 가져오기
    csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".csv")]
    
    if not csv_files:
        print("처리할 CSV 파일을 찾을 수 없습니다.")
        print(f"CSV 파일을 다음 위치에 복사해주세요: {folder_path}")
        input("계속하려면 아무 키나 누르세요...")
        return

    for channel_num in BASE_CONFIG['channels_range']:
        row_index = channel_num
        results = []
        
        for csv_file in csv_files:
            try:
                csv_path = os.path.join(folder_path, csv_file)
                
                if not os.path.exists(csv_path):
                    print(f"파일을 찾을 수 없음: {csv_path}")
                    continue
                
                # trayID 추출
                match_tray = re.search(r"_TrayID_(.*?)_", csv_file)
                if not match_tray:
                    print(f"TrayID를 찾을 수 없음: {csv_file}")
                    tray_id = "Unknown"
                else:
                    tray_id = match_tray.group(1)

                # CSV 읽기
                try:
                    data = read_csv_columns(csv_path, config['col_channel_id'], config['col_data_end'])
                    
                    if len(data) <= row_index:
                        continue

                    # 시간 데이터 추출 (첫 번째 행)
                    time_values = data[0][1:]
                    
                    # channel 데이터 추출
                    channel_id_cell = data[row_index][0]
                    channel_values = data[row_index][1:]
                    
                    # 결과 저장
                    row_data = [tray_id, channel_id_cell] + channel_values
                    if len(results) == 0:
                        time_row = ["Time", "Time"] + time_values
                        results.append(time_row)
                    results.append(row_data)
                    
                except Exception as e:
                    print(f"CSV 처리 중 오류 발생 ({csv_file}): {str(e)}")
                    continue
                
            except Exception as e:
                print(f"처리 중 오류 발생: {str(e)}")
                continue
        
        if not results:
            print(f"채널 {channel_num} 추출 결과가 없습니다.")
            continue
        
        # 결과 저장을 위한 전처리
        max_len = max(len(r) for r in results) - 2
        
        # 결과가 짧은 행은 None으로 채우기
        for r in results:
            diff = (2 + max_len) - len(r)
            if diff > 0:
                r.extend([''] * diff)
        
        # 결과를 전치(transpose)하여 저장
        transposed_results = list(map(list, zip(*results)))
        
        # CSV 파일로 저장
        output_csv = os.path.join(ext_folder, f"Ch{channel_num:02d}_{config['name']}.csv")
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(transposed_results)
        
        print(f"채널 {channel_num} {config['name']} 추출 완료 -> {output_csv}")

# 메인 실행
if __name__ == "__main__":
    print(f"데이터 처리를 시작합니다.")
    print(f"작업 폴더: {BASE_CONFIG['folder_path']}")
    print(f"CSV 파일은 이 실행 파일과 같은 폴더에 있어야 합니다.")
    print("---------------------------------------------")
    
    # 전류 데이터 추출
    extract_data('current', DATA_CONFIG['current'])
    
    # 전압 데이터 추출
    extract_data('voltage', DATA_CONFIG['voltage'])
    
    print("---------------------------------------------")
    print("모든 처리가 완료되었습니다.")
    print(f"결과는 'output' 폴더에 저장되었습니다: {os.path.join(BASE_CONFIG['folder_path'], 'output')}")
    #input("프로그램을 종료하려면 아무 키나 누르세요...")