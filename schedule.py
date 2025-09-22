import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QMovie

class DeskPet(QWidget):
    def __init__(self):
        super().__init__()

        # ===== 桌面宠物动画 =====
        self.pet_label = QLabel()
        self.movie = QMovie("dragon_wave.gif")  # 替换为你的 GIF
        self.pet_label.setMovie(self.movie)
        self.movie.start()

        # ===== 日程输入区 =====
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("输入日程：YYYY-MM-DD HH:MM 事件")
        self.add_button = QPushButton("添加日程")
        self.add_button.clicked.connect(self.add_schedule)

        self.schedule_display = QTextEdit()
        self.schedule_display.setReadOnly(True)

        self.schedules = []  # 保存用户添加的日程

        # ===== 布局 =====
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.pet_label)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.input_line)
        v_layout.addWidget(self.add_button)
        v_layout.addWidget(self.schedule_display)

        h_layout.addLayout(v_layout)
        self.setLayout(h_layout)

        # ===== 窗口属性 =====
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

        # ===== 定时检查日程 =====
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_schedule)
        self.timer.start(60000)  # 每分钟检查一次

        # 鼠标拖动变量
        self.dragging = False

    # 添加日程
    def add_schedule(self):
        text = self.input_line.text().strip()
        if not text:
            return
        try:
            date_str, time_str, *event = text.split()
            dt_str = f"{date_str} {time_str}"
            QDateTime.fromString(dt_str, "yyyy-MM-dd HH:mm")  # 校验格式
            event_str = " ".join(event)
            self.schedules.append({"datetime": dt_str, "event": event_str})
            self.schedule_display.append(f"{dt_str} - {event_str}")
            self.input_line.clear()
        except:
            QMessageBox.warning(self, "错误", "日程格式错误，请使用 YYYY-MM-DD HH:MM 事件")

    # 检查日程
    def check_schedule(self):
        now = QDateTime.currentDateTime()
        for item in self.schedules:
            dt = QDateTime.fromString(item["datetime"], "yyyy-MM-dd HH:mm")
            if now.secsTo(dt) <= 15*60 and now.secsTo(dt) > 0:
                QMessageBox.information(self, "日程提醒", f"📅 主人，{item['event']} 快开始啦！")

    # 鼠标拖动宠物
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        self.dragging = False

# ===== 主程序 =====
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DeskPet()
    sys.exit(app.exec())
