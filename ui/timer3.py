import tkinter as tk
from tkinter import ttk
import time

class TimerApp:
    def __init__(self, root):
        # 전체 배경색 상수 정의
        self.BG_COLOR = "#ffffff"  # 순수 흰색
        
        self.root = root
        self.root.title("타이머")
        
        # 비율 상수 정의
        self.RATIO_WIDTH = 4
        self.RATIO_HEIGHT = 1.5
        self.BASE_WIDTH = 400
        self.BASE_HEIGHT = int(self.BASE_WIDTH * (self.RATIO_HEIGHT / self.RATIO_WIDTH))
        
        # 초기 창 크기 설정
        self.root.geometry(f"{self.BASE_WIDTH}x{self.BASE_HEIGHT}")
        
        # 최소/최대 크기 설정 (비율 유지)
        min_width = 200
        min_height = int(min_width * (self.RATIO_HEIGHT / self.RATIO_WIDTH))
        max_width = 600
        max_height = int(max_width * (self.RATIO_HEIGHT / self.RATIO_WIDTH))
        
        self.root.minsize(min_width, min_height)
        self.root.maxsize(max_width, max_height)
        self.root.configure(bg=self.BG_COLOR)
        
        # 스타일 설정
        self.style = ttk.Style()
        # 프레임 스타일 설정
        self.style.configure("TFrame", background=self.BG_COLOR)
        
        # 레이블 스타일 설정
        self.style.configure("Timer.TLabel",
                           font=("Segoe UI", 32),
                           background=self.BG_COLOR,  # 배경색 통일
                           foreground="#0078D4")
        
        # 버튼 스타일 설정
        self.style.configure("Control.TButton",
                           font=("Segoe UI", 10))
        
        # 메인 프레임 - 비율 조정 (8:3 = 4:1.5와 동일한 비율)
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(expand=True, fill="both")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=8)    # 시간표시 영역
        self.main_frame.grid_rowconfigure(1, weight=3)    # 버튼 영역
        
        # 창 크기 조정 이벤트 바인딩
        self.root.bind('<Configure>', self.on_resize)
        
        # 시간 표시 프레임
        self.time_frame = ttk.Frame(self.main_frame)
        self.time_frame.grid(row=0, column=0, sticky="nsew", padx=10)  # 좌우 여백 추가
        self.time_frame.grid_columnconfigure(0, weight=1)
        self.time_frame.grid_rowconfigure(0, weight=1)
        
        # 시간 표시
        self.time_var = tk.StringVar()
        self.time_var.set("00:00:00.000")
        
        self.label = ttk.Label(self.time_frame, 
                             textvariable=self.time_var,
                             style="Timer.TLabel",
                             anchor="center")  # 중앙 정렬
        self.label.grid(row=0, column=0)
        
        # 버튼 프레임 수정
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, sticky="ew", padx=20)  # 좌우 여백 증가
        
        # 버튼 프레임 열 비율 조정
        self.button_frame.grid_columnconfigure(0, weight=4)  # 첫 번째 버튼
        self.button_frame.grid_columnconfigure(1, weight=1)  # 간격
        self.button_frame.grid_columnconfigure(2, weight=4)  # 두 번째 버튼
        
        # 버튼 배치 수정
        self.start_stop_button = ttk.Button(
            self.button_frame,
            text="시작",
            command=self.toggle_timer,
            style="Control.TButton"
        )
        self.start_stop_button.grid(row=0, column=0, pady=5, sticky="ew")  # 여백 축소
        
        self.reset_button = ttk.Button(
            self.button_frame,
            text="초기화",
            command=self.reset_timer,
            style="Control.TButton"
        )
        self.reset_button.grid(row=0, column=2, pady=5, sticky="ew")  # 여백 축소
        
        # 상태 변수
        self.is_running = False
        self.start_time = None
        self.update_interval = 16
        
        # 윈도우 투명도
        self.root.attributes('-alpha', 0.95)
        
        # 폰트 크기 동적 조정을 위한 바인딩
        self.root.bind('<Configure>', self.on_resize)
        
        # 초기 폰트 크기 설정
        self.adjust_font_size()
    
    def on_resize(self, event):
        """창 크기 조정 시 처리"""
        if event.widget == self.root:
            # 현재 창 크기
            current_width = self.root.winfo_width()
            current_height = self.root.winfo_height()
            
            # 너비 기준으로 높이 계산
            desired_height = int(current_width * (self.RATIO_HEIGHT / self.RATIO_WIDTH))
            
            # 현재 높이가 원하는 높이와 다르면 조정
            if abs(current_height - desired_height) > 2:  # 2픽셀 이상 차이나면 조정
                self.root.geometry(f"{current_width}x{desired_height}")
            
            # 폰트 크기 조정
            self.adjust_font_size()
    
    def adjust_font_size(self, event=None):
        """윈도우 크기에 따라 폰트 크기 조정"""
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # 시간 표시 폰트 크기 계산
        base_size = min(window_width // 10, window_height // 3)
        time_font_size = max(20, min(base_size, 42))
        
        # 버튼 폰트 크기 계산
        button_font_size = max(8, min(base_size // 4, 11))
        
        # 스타일 업데이트
        self.style.configure("Timer.TLabel", 
                           font=("Segoe UI", time_font_size))
        self.style.configure("Control.TButton", 
                           font=("Segoe UI", button_font_size))
    
    def toggle_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_stop_button['text'] = "시작"
        else:
            self.is_running = True
            self.start_time = time.perf_counter()
            self.update_timer()
            self.start_stop_button['text'] = "중지"
    
    def reset_timer(self):
        self.is_running = False
        self.start_time = None
        self.time_var.set("00:00:00.000")
        self.start_stop_button['text'] = "시작"
    
    def update_timer(self):
        if self.is_running and self.start_time is not None:
            try:
                current_time = time.perf_counter()
                elapsed_time = current_time - self.start_time
                
                total_milliseconds = int(elapsed_time * 1000)
                hours = total_milliseconds // 3600000
                remainder = total_milliseconds % 3600000
                minutes = remainder // 60000
                remainder = remainder % 60000
                seconds = remainder // 1000
                milliseconds = remainder % 1000
                
                self.time_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")
                
                self.root.after(self.update_interval, self.update_timer)
            except Exception as e:
                print(f"타이머 업데이트 오류: {e}")
                self.reset_timer()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
