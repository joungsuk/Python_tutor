import csv
import re
import argparse

#NFF 직렬형 충방전기 테스트 UI의 csv 결과 데이터에서 시간과 전류를 추출

def extract_time_and_current(lines):
    data = []
    
    for line in lines:
        line = line.strip()  # 각 줄의 앞뒤 공백 제거
        
        # 시간 데이터 추출
        time_match = re.search(r'\[(\d{2}:\d{2}:\d{2}\.\d{3})\]', line)
        if time_match:
            time_data = time_match.group(1)
        else:
            continue  # 시간 데이터가 없으면 다음 줄로 넘어감
        
        # 전류 데이터 추출 (행에서 5번째 값)
        parts = line.split(',')
        if len(parts) > 5:  # 전류 값이 존재하는지 확인
            current_data = parts[5].strip()  # 5번째 인덱스의 전류 값
            data.append({"Time": time_data, "Current (A)": current_data})
    
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
    
    # EUC-KR 인코딩을 사용하여 파일을 읽기
    with open(input_file, 'r', encoding='EUC-KR') as f:
        lines = f.readlines()
    
    # 시간과 전류 추출
    extracted_data = extract_time_and_current(lines)
    
    # CSV 파일로 저장
    write_to_csv(extracted_data, output_file)

if __name__ == "__main__":
    main()
