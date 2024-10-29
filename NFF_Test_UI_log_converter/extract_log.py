import csv
import re
import argparse
import chardet

#NFF 직렬형 충방전기 테스트 UI의 txt 로그에서 시간과 전류를 추출

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # 파일의 처음 10000 바이트 읽기
    result = chardet.detect(raw_data)
    return result['encoding']


def extract_time_and_current(lines):
    data = []
    filtered_lines = [line for line in lines if line.strip()]  # 빈 줄 제거
    
    i = 0
    while i < len(filtered_lines):
        # 첫 번째 줄에서 시간 추출
        time_match = re.search(r'\[(\d{2}:\d{2}:\d{2}\.\d{3})\]', filtered_lines[i])
        if time_match:
            time_data = time_match.group(1)
        else:
            i += 1
            continue  # 시간 데이터가 없으면 다음 줄로 넘어감

        # 전류 데이터가 있는 줄을 찾음
        if i + 1 < len(filtered_lines):
            current_match = re.search(r'Cur\s([-+]?\d+\.\d{3})A', filtered_lines[i + 1])
            if current_match:
                current_data = current_match.group(1)
                data.append({"Time": time_data, "Current (A)": current_data})
            else:
                print(f"Current data not found in line: {filtered_lines[i + 1]}")
        i += 2  # 두 줄을 처리했으므로 2씩 증가

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
    # 입력 파일과 출력 파일 이름을 직접 지정
    #input_file = "test.txt"  # 입력 파일 이름
    #output_file = "test.csv"  # 출력 파일 이름
    
    # 파일 인코딩 감지 및 텍스트로 변환
    #result = from_path(input_file).best()
    #text = result.raw.decode(result.encoding)  # 바이너리 데이터를 감지된 인코딩으로 디코딩
    
    #lines = text.splitlines()

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
