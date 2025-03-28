import os

# CSV 파일이 있는 폴더 경로
folder_path = 'd:/tmp/cal'
output_file = 'd:/tmp/cal/output.txt'

with open(output_file, 'w', encoding='utf-8') as outfile:
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='EUC-KR') as csvfile:  # CSV 파일을 직접 열기
                lines = csvfile.readlines()  # 모든 줄을 읽기
                if len(lines) >= 5:  # 5번째 줄이 있는지 확인
                    cal_data = lines[4].strip()  # 5번째 줄 추출 및 공백 제거
                    '''
                    # 쉼표 뒤의 공백을 제거하기 위해 cal_data 처리
                    cleaned_line = '\t'.join(part.strip() for part in cal_data.split(','))  # 각 부분의 공백 제거
                    # 파일 이름에서 확장자 제거
                    filename_without_extension = os.path.splitext(filename)[0]  # 확장자 제거
                    # 파일 이름과 3번째 줄 내용을 탭으로 구분하여 저장
                    outfile.write(f"{filename_without_extension}\t{cleaned_line}\n")
                    '''
                    # 파일 이름에서 확장자 제거
                    filename_without_extension = os.path.splitext(filename)[0]  # 확장자 제거
                    # 파일 이름과 3번째 줄 내용을 탭으로 구분하여 저장
                    outfile.write(f"{filename_without_extension}, {cal_data}\n")