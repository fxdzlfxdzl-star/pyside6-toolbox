"""
示例 01 —— 第一个 PySide6 窗口

用法::

    python examples/01_hello_window.py              # 打开窗口
    python examples/01_hello_window.py --selftest   # 自检，不开窗口

对照点（都是 PyQt5 老手最容易踩的）：
  1. 导入路径          PyQt5.QtWidgets  ->  PySide6.QtWidgets
  2. 信号定义          pyqtSignal       ->  Signal
  3. 槽装饰器          pyqtSlot         ->  Slot
  4. 事件循环          app.exec_()      ->  app.exec()   （exec_ 仍保留为兼容别名，但已弃用）
  5. 枚举              Qt.AlignCenter   ->  Qt.AlignmentFlag.AlignCenter（推荐全限定名）
  6. QAction/QShortcut 从 QtWidgets    ->  QtGui
"""

import sys

from PySide6.QtCore import Qt
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


def run_selftest() -> int:
    """自检：不开窗口，验证窗口能构建、信号槽能触发。返回 0 表示通过。"""
    failures: list[str] = []

    def check(name: str, cond: bool, detail: str = "") -> None:
        print(f"  [{'OK  ' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
        if not cond:
            failures.append(name)

    app = QApplication.instance() or QApplication(sys.argv)

    print("== 窗口构建 ==")
    window = MainWindow()
    check("主窗口创建成功", window is not None)
    check("窗口标题正确", window.windowTitle() == "Hello PySide6", window.windowTitle())
    check("初始文案正确", window.label.text() == "你好，PySide6！", window.label.text())

    print("== 信号槽 ==")
    window.button.click()
    check("点击一次后计数为 1", window._count == 1, f"_count={window._count}")
    check("文案已更新", window.label.text() == "被点了 1 次", window.label.text())
    window.button.click()
    check("点击两次后计数为 2", window._count == 2, f"_count={window._count}")

    print("== 事件循环 API ==")
    check("app.exec 存在（推荐）", hasattr(app, "exec"))
    check("app.exec_ 保留为兼容别名（已弃用）", hasattr(app, "exec_"))

    print()
    if failures:
        print(f"结果：{len(failures)} 项未通过 -> {failures}")
        return 1
    print("结果：全部通过")
    return 0


def main() -> int:
    if "--selftest" in sys.argv:
        return run_selftest()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()  # PyQt5 写的是 app.exec_()


if __name__ == "__main__":
    sys.exit(main())
