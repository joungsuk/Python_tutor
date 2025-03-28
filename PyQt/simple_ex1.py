import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("테스트 UI")
        self.setGeometry(100, 100, 400, 200)

        # 중앙 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 입력 필드
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        # 버튼
        self.test_button = QPushButton("테스트 실행")
        self.test_button.clicked.connect(self.run_test)
        layout.addWidget(self.test_button)

        # 결과 표시 레이블
        self.result_label = QLabel("결과가 여기에 표시됩니다")
        layout.addWidget(self.result_label)

    def run_test(self):
        # 테스트 로직
        input_text = self.input_field.text()
        self.result_label.setText(f"입력값: {input_text}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())