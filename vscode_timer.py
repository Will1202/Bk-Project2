import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMessageBox
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer
import Quartz


def get_frontmost_app():
    """获取当前前台应用名 (macOS)"""
    workspace = Quartz.NSWorkspace.sharedWorkspace()
    app = workspace.frontmostApplication()
    return app.localizedName()


class Pet(QLabel):
    def __init__(self):
        super().__init__()

        # GIF 路径
        gif_path = "/Users/Christy/CSProj2/Gif_527.gif"
        self.movie = QMovie(gif_path)

        if not self.movie.isValid():
            print(f"❌ GIF 加载失败: {gif_path}")
            self.setText("GIF 加载失败！")
            self.resize(200, 100)
            # 普通窗口调试模式
            self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        else:
            print(f"✅ GIF 加载成功: {gif_path}")
            self.setMovie(self.movie)
            self.movie.start()

            # 🔹 让窗口大小匹配 GIF 大小
            self.resize(self.movie.currentPixmap().size())

            # 桌宠模式：无边框 + 透明背景 + 置顶
            self.setWindowFlags(Qt.FramelessWindowHint |
                                Qt.WindowStaysOnTopHint |
                                Qt.SubWindow)
            self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 初始位置
        self.move(300, 300)
        self.show()

        # 计时器
        self.vscode_time = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_vscode)
        self.timer.start(1000)  # 每秒检测一次

    def check_vscode(self):
        app_name = get_frontmost_app()
        print("当前应用:", app_name)

        # VS Code 有时是 "Code"，有时是 "Python"
        if "Code" in app_name or "Python" in app_name:
            self.vscode_time += 1
            print(f"VS Code 已运行 {self.vscode_time} 秒")

            if self.vscode_time == 20:
                QMessageBox.information(self, "提示", "你已经打开 VS Code 30 秒啦！")
        else:
            # 切换到其他应用就清零（如果你想累计，可以改逻辑）
            self.vscode_time = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = Pet()
    sys.exit(app.exec_())
