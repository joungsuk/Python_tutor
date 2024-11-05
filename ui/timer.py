import tkinter as tk
from tkinter import messagebox
import time
from typing import Optional
from dataclasses import dataclass
import winsound

@dataclass
class TimerState:
    is_running: bool = False
    start_time: Optional[float] = None
    countdown_seconds: Optional[int] = None

class TimerApp:
    # 상수 정의
    UPDATE_INTERVAL: int = 1000  # 타이머 업데이트 간격 (ms)
    DEFAULT_TIME: str = "00:00:00"
    ALERT_FREQUENCY: int = 2500  # 알림음 주파수
    ALERT_DURATION: int = 1000   # 알림음 지속시간 (ms)

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("타이머 프로그램")
        self.root.geometry("400x350")
        
        self.state = TimerState()
        self.setup_variables()
        self.create_widgets()
        self.bind_shortcuts()

    def setup_variables(self) -> None:
        """타이머 변수 초기화"""
        self.time_var = tk.StringVar(value=self.DEFAULT_TIME)
        self.mode_var = tk.StringVar(value="스톱워치")

    def create_widgets(self) -> None:
        """UI 위젯 생성"""
        # 모드 선택
        self.create_mode_selector()
        
        # 시간 입력 프레임
        self.create_time_input()
        
        # 타이머 표시
        self.label = tk.Label(self.root, textvariable=self.time_var, font=("Helvetica", 24))
        self.label.pack(pady=20)
        
        # 버튼 프레임
        self.create_buttons()

    def create_mode_selector(self) -> None:
        """모드 선택 라디오 버튼 생성"""
        modes_frame = tk.Frame(self.root)
        modes_frame.pack(pady=10)
        
        tk.Radiobutton(modes_frame, text="스톱워치", variable=self.mode_var, 
                      value="스톱워치", command=self.mode_changed).pack(side="left", padx=10)
        tk.Radiobutton(modes_frame, text="카운트다운", variable=self.mode_var, 
                      value="카운트다운", command=self.mode_changed).pack(side="left", padx=10)

    def create_time_input(self) -> None:
        """시간 입력 필드 생성"""
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)
        
        # 시간 입력
        self.hours_var = tk.StringVar(value="00")
        self.minutes_var = tk.StringVar(value="00")
        self.seconds_var = tk.StringVar(value="00")
        
        tk.Entry(self.input_frame, textvariable=self.hours_var, width=3).pack(side="left")
        tk.Label(self.input_frame, text=":").pack(side="left")
        tk.Entry(self.input_frame, textvariable=self.minutes_var, width=3).pack(side="left")
        tk.Label(self.input_frame, text=":").pack(side="left")
        tk.Entry(self.input_frame, textvariable=self.seconds_var, width=3).pack(side="left")

    def create_buttons(self) -> None:
        """버튼 생성"""
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_stop_button = tk.Button(button_frame, text="시작", command=self.toggle_timer)
        self.start_stop_button.pack(side="left", padx=5)
        
        self.reset_button = tk.Button(button_frame, text="초기화", command=self.reset_timer)
        self.reset_button.pack(side="left", padx=5)

    def bind_shortcuts(self) -> None:
        """단축키 바인딩"""
        self.root.bind('<space>', lambda e: self.toggle_timer())
        self.root.bind('<Return>', lambda e: self.toggle_timer())
        self.root.bind('<r>', lambda e: self.reset_timer())

    def mode_changed(self) -> None:
        """모드 변경 시 처리"""
        self.reset_timer()
        self.input_frame.pack() if self.mode_var.get() == "카운트다운" else self.input_frame.pack_forget()

    def get_countdown_seconds(self) -> int:
        """입력된 시간을 초 단위로 변환"""
        try:
            hours = int(self.hours_var.get())
            minutes = int(self.minutes_var.get())
            seconds = int(self.seconds_var.get())
            return hours * 3600 + minutes * 60 + seconds
        except ValueError:
            messagebox.showerror("입력 오류", "올바른 시간을 입력하세요")
            return 0

    def toggle_timer(self) -> None:
        """타이머 시작/정지 토글"""
        try:
            if self.state.is_running:
                self.state.is_running = False
                self.start_stop_button['text'] = "시작"
            else:
                self.state.is_running = True
                if self.mode_var.get() == "카운트다운":
                    self.state.countdown_seconds = self.get_countdown_seconds()
                self.state.start_time = time.monotonic()
                self.update_timer()
                self.start_stop_button['text'] = "정지"
        except Exception as e:
            messagebox.showerror("오류", f"타이머 작동 중 오류가 발생했습니다: {str(e)}")

    def reset_timer(self) -> None:
        """타이머 초기화"""
        self.state = TimerState()
        self.time_var.set(self.DEFAULT_TIME)
        self.start_stop_button['text'] = "시작"

    def update_timer(self) -> None:
        """타이머 업데이트"""
        if not self.state.is_running:
            return

        try:
            elapsed = time.monotonic() - self.state.start_time

            if self.mode_var.get() == "카운트다운":
                remaining = max(0, self.state.countdown_seconds - int(elapsed))
                if remaining == 0:
                    self.timer_complete()
                    return
                self.update_display(remaining)
            else:  # 스톱워치 모드
                self.update_display(int(elapsed))

            self.root.after(self.UPDATE_INTERVAL, self.update_timer)
        except Exception as e:
            messagebox.showerror("오류", f"타이머 업데이트 중 오류가 발생했습니다: {str(e)}")

    def update_display(self, total_seconds: int) -> None:
        """화면 표시 업데이트"""
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.time_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def timer_complete(self) -> None:
        """타이머 완료 처리"""
        self.state.is_running = False
        self.start_stop_button['text'] = "시작"
        winsound.Beep(self.ALERT_FREQUENCY, self.ALERT_DURATION)
        messagebox.showinfo("알림", "타이머가 완료되었습니다!")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TimerApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("치명적 오류", f"프로그램 실행 중 오류가 발생했습니다: {str(e)}")
