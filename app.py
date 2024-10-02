import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import sys
import time

class ClickerThread(QThread):
    stopped = pyqtSignal()

    def __init__(self, x, y, interval, clicks):
        super().__init__()
        self.x = x
        self.y = y
        self.interval = interval
        self.clicks = clicks
        self.running = True

    def run(self):
        click_count = 0
        while self.running:
            if self.clicks != 0 and click_count >= self.clicks:
                break
            pyautogui.click(self.x, self.y)
            click_count += 1
            print(f"클릭 {click_count}회 실행됨")
            time.sleep(self.interval)
        self.stopped.emit()

    def stop(self):
        self.running = False


class AutoClicker(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.clicker_thread = None
        self.x, self.y = None, None
        self.is_running = False  # 매크로가 실행 중인지 여부를 나타내는 플래그

    def initUI(self):
        layout = QVBoxLayout()

        self.interval_label = QLabel('인터벌 (초):', self)
        layout.addWidget(self.interval_label)

        self.interval_input = QLineEdit(self)
        self.interval_input.setText("1")
        layout.addWidget(self.interval_input)

        self.clicks_label = QLabel('클릭 횟수 (무한: 0):', self)
        layout.addWidget(self.clicks_label)

        self.clicks_input = QLineEdit(self)
        self.clicks_input.setText("0")
        layout.addWidget(self.clicks_input)

        self.setLayout(layout)
        self.setWindowTitle('Auto Clicker')
        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.save_coords()
        elif event.key() == Qt.Key_Escape:
            self.stop_clicking()
        elif event.key() == Qt.Key_Shift:
            self.toggle_macro()  # Shift 키를 누르면 매크로 시작/종료 전환

    def save_coords(self):
        self.x, self.y = pyautogui.position()
        print(f"좌표 저장됨: ({self.x}, {self.y})")
        QMessageBox.information(self, '좌표 저장', '좌표가 저장되었습니다!')

    def toggle_macro(self):
        if not self.is_running:
            self.start_clicking()
        else:
            self.stop_clicking()

    def start_clicking(self):
        if self.x is None or self.y is None:
            print("좌표를 저장하세요!")
            QMessageBox.warning(self, '경고', '좌표가 저장되지 않았습니다!')
            return
        try:
            interval = float(self.interval_input.text())
            clicks = int(self.clicks_input.text())
            self.clicker_thread = ClickerThread(self.x, self.y, interval, clicks)
            self.clicker_thread.stopped.connect(self.on_clicking_stopped)
            self.clicker_thread.start()
            self.is_running = True  # 매크로가 실행 중임을 나타냄
            print("매크로 시작됨")
        except ValueError:
            print("올바른 값을 입력하세요!")
            QMessageBox.warning(self, '오류', '올바른 값을 입력하세요!')

    def stop_clicking(self):
        if self.clicker_thread:
            self.clicker_thread.stop()
        self.is_running = False  # 매크로가 종료되었음을 나타냄
        QMessageBox.information(self, '매크로 종료', '매크로가 종료되었습니다')
        print("매크로 종료됨")

    def on_clicking_stopped(self):
        print("클릭이 완료되었습니다.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutoClicker()
    sys.exit(app.exec_())
