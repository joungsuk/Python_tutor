# 기본 창 만들기
import sys
#from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QAction,
    QDockWidget,
    QPushButton,      # 버튼
    QVBoxLayout,      # 수직 레이아웃
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("첫 번째 앱")
        self.setGeometry(100, 100, 400, 300)  # x, y, width, height
        
                # 1. 메뉴바
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('파일')
        editMenu = menubar.addMenu('편집')
        
        # 메뉴 항목 추가
        newAction = QAction('새로 만들기', self)
        fileMenu.addAction(newAction)
        
        editAction = QAction('오리기', self)
        editMenu.addAction(editAction)
        
        
        # 2. 툴바
        toolbar = self.addToolBar('메인 툴바')
        
        # 툴바에 액션 추가
        newAction = QAction(QIcon('new.png'), '새로 만들기', self)
        toolbar.addAction(newAction)
        
        # 3. 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # 여백 설정
        layout.setContentsMargins(10, 10, 10, 10)  # 좌, 상, 우, 하
        
        # 위젯 간격 설정
        layout.setSpacing(20)
        
        # 정렬 설정
        layout.setAlignment(Qt.AlignTop)
        
        # 위젯 추가시 정렬 지정
        layout.addWidget(QPushButton("버튼"), alignment=Qt.AlignCenter)
        layout.addWidget(QPushButton("버튼2"), alignment=Qt.AlignCenter)

        
        # 4. 상태바
        status_bar = self.statusBar()
        
        self.status_label = QLabel("상태:")
        status_bar.addPermanentWidget(self.status_label)
        
        # 2. 임시 메시지 표시 (3초)
        status_bar.showMessage("작업 완료", 3000)
        
        # 3. 여러 위젯 추가
        self.count_label = QLabel("항목: 0개")
        status_bar.addPermanentWidget(self.count_label)
        
        # 4. 상태바 스타일 설정
        status_bar.setStyleSheet("QStatusBar{background:lightgray;}")
        
        # 5. 도킹 위젯
        dock = QDockWidget('도킹 위젯', self)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())