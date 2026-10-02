"""
示例 01 —— 第一个 PySide6 窗口

对照点（都是 PyQt5 老手最容易踩的）：
  1. 导入路径          PyQt5.QtWidgets  ->  PySide6.QtWidgets
  2. 信号定义          pyqtSignal       ->  Signal
  3. 槽装饰器          pyqtSlot         ->  Slot
  4. 事件循环          app.exec_()      ->  app.exec()      （只有一个 exec）
  5. 枚举              Qt.AlignCenter   ->  Qt.AlignmentFlag.AlignCenter（推荐全限定名）
  6. QAction/QShortcut 从 QtWidgets    ->  QtGui
"""

import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Hello PySide6")
        self.resize(480, 320)

        self._count = 0

        central = QWidget()
        layout = QVBoxLayout(central)

        self.label = QLabel("你好，PySide6！")
        # PyQt5 写法是 Qt.AlignCenter；PySide6 两种都支持，但推荐显式枚举
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.button = QPushButton("点我")
        # 信号槽连接语法与 PyQt5 完全一致
        self.button.clicked.connect(self.on_clicked)
        layout.addWidget(self.button)

        self.setCentralWidget(central)

    def on_clicked(self) -> None:
        self._count += 1
        self.label.setText(f"被点了 {self._count} 次")


def main() -> int:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()  # PyQt5 写的是 app.exec_()


if __name__ == "__main__":
    sys.exit(main())
