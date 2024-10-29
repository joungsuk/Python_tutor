import csv
import argparse
from datetime import datetime
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # 파일의 처음 10000 바이트 읽기
    result = chardet.detect(raw_data)
    return result['encoding']

def extract_time_and_current(lines):
    data = []
    previous_time = None  # 이전 시간 값을 저장할 변수

    for line in lines:
        line = line.strip()  # 각 줄의 앞뒤 공백 제거
        
        if line.startswith("Time (s)"):  # 헤더 줄을 건너뛰기
            continue
        
        # 데이터 추출
        parts = line.split(',')
        if len(parts) >= 2:  # 데이터가 두 개 이상인지 확인
            time_str = parts[0].strip()  # 첫 번째 인덱스에서 시간 문자열 추출
            current_str = parts[1].strip()  # 두 번째 인덱스에서 전류 문자열 추출
            
            # 시간 변환: "2024-10-15 14:59:29.172" => "14:59:29"
            time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
            milliseconds = int(round(time_obj.microsecond / 1000.0))
            #formatted_time = time_obj.strftime("%H:%M:%S.%f")  # 초까지 포맷팅
            formatted_time = time_obj.strftime(f"%H:%M:%S.{milliseconds:03d}")  # 초까지 포맷팅
            
            # 동일 초 체크
            if formatted_time != previous_time:
                previous_time = formatted_time  # 이전 시간 값 업데이트
                # 전류 데이터 변환: 부동소수점으로 변환 후 1e6 곱하기
                try:
                    current_data = float(current_str) * 1e6  # 전류 값을 부동소수점으로 변환하고 1e6을 곱함
                    # 소수점 3자리로 포맷팅
                    current_data_formatted = format(current_data, '.3f')
                    data.append({"Time": formatted_time, "Current (A)": current_data_formatted})
                except ValueError:
                    print(f"Invalid current data: {current_str}")
    
    return data

def write_to_csv(data, output_file):
    if data:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Time", "Current (A)"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully written to {output_file}")
    else:
        print("No data to write.")

def main():
    # 커맨드 라인 인자 처리
    parser = argparse.ArgumentParser(description='Extract time and current data from log file.')
    parser.add_argument('input_file', type=str, help='Input log file path')
    parser.add_argument('output_file', type=str, help='Output CSV file path')
    
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    
    # 파일 인코딩 감지
    encoding = detect_encoding(input_file)
    print(f"Detected encoding: {encoding}")
    
    # 감지된 인코딩을 사용하여 파일을 읽기
    with open(input_file, 'r', encoding=encoding) as f:
        lines = f.readlines()
    
    # 시간과 전류 추출
    extracted_data = extract_time_and_current(lines)
    
    # CSV 파일로 저장
    write_to_csv(extracted_data, output_file)

if __name__ == "__main__":
    main()
