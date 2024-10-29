import tkinter as tk

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("타이머 프로그램")
        self.root.geometry("400x250")
        
        self.time_var = tk.StringVar()
        self.time_var.set("00:00:01")
        
        self.label = tk.Label(root, textvariable=self.time_var, font=("Helvetica", 24), fg="white", bg="blue")
        self.label.pack(pady=20)
        
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()
        
        self.start_stop_button = tk.Button(self.button_frame, text="시작/중지", command=self.toggle_timer, bg="purple", fg="white")
        self.start_stop_button.pack(side="left", padx=(0, 40))
        
        self.reset_button = tk.Button(self.button_frame, text="초기화", command=self.reset_timer, bg="purple", fg="white")
        self.reset_button.pack(side="left")
        
        self.is_running = False
        self.start_time = None

    def toggle_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_stop_button['text'] = "시작"
        else:
            self.is_running = True
            self.start_time = time.time()
            self.update_timer()
            self.start_stop_button['text'] = "중지"
    
    def reset_timer(self):
        self.is_running = False
        self.start_time = None
        self.time_var.set("00:00:01")
        self.start_stop_button['text'] = "시작"
    
    def update_timer(self):
        if self.is_running:
            elapsed_time = int(time.time() - self.start_time)
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
