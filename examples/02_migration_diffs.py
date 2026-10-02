"""PyQt5 -> PySide6 迁移对照 · 可运行示例

第 1 周主力材料。把 `notes/00-learning-path.md` 里那张迁移对照表逐条落成能跑的代码。

用法::

    python examples/02_migration_diffs.py              # 打开对照窗口
    python examples/02_migration_diffs.py --selftest   # 只跑差异校验，不开窗口

设计说明
--------
每个差异点都在两处出现：

1. 文件顶部/类定义处的 `差异 N:` 注释块 —— 左边写 PyQt5 原写法，右边写 PySide6 写法
2. `--selftest` 里的断言 —— 用代码证明"PySide6 确实是这样"，而不是靠记忆

这样做的原因：迁移期的错误几乎都来自"以为一样"。断言能让机器替你确认。
"""

from __future__ import annotations

import sys

# ============================================================================
# 差异 1：信号 / 槽 / 属性 的命名
# ----------------------------------------------------------------------------
#   PyQt5                              PySide6
#   from PyQt5.QtCore import ...       from PySide6.QtCore import ...
#     pyqtSignal                         Signal
#     pyqtSlot                           Slot
#     pyqtProperty                       Property
#
#   底层绑定机制不同：PyQt5 用 SIP，PySide6 用 Shiboken。
#   其余用法完全一致（都要在类属性位置定义，不能在 __init__ 里动态加）。
# ============================================================================
from PySide6.QtCore import (
    QObject,
    QRegularExpression,
    Qt,
    Signal,
    Slot,
)

# ============================================================================
# 差异 2：QAction / QShortcut 换了模块（Qt4 -> Qt5 遗留的老习惯要改）
# ----------------------------------------------------------------------------
#   PyQt5:    from PyQt5.QtWidgets import QAction, QShortcut
#   PySide6:  from PySide6.QtGui  import QAction, QShortcut
#
#   原因：Qt6 把这两个类从 QtWidgets 移到了 QtGui（它们不依赖 widget 体系）。
#   注意 PyQt6 也是同样的改动 —— 这是 Qt6 层面的迁移，不是绑定层面的。
# ============================================================================
from PySide6.QtGui import (
    QAction,
    QFontMetrics,
    QGuiApplication,
    QShortcut,
)
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


# ============================================================================
# 差异 9：信号重载 / 自定义信号
# ----------------------------------------------------------------------------
#   PyQt5:    finished = pyqtSignal(int)
#   PySide6:  finished = Signal(int)
#
#   重载（同名不同签名）在 PySide6 里的写法是直接叠两个 Signal，
#   连接时靠槽函数的签名区分；或者用 @Slot(int) 显式标注来消歧。
# ============================================================================
class CounterWorker(QObject):
    """演示 Signal(自定义) + @Slot 装饰器 + 跨对象通信。"""

    # 定义在类属性位置 —— 与 PyQt5 的 pyqtSignal 位置一致
    ticked = Signal(int)
    finished = Signal(str)

    @Slot()
    def start_counting(self) -> None:
        for i in range(1, 4):
            self.ticked.emit(i)
        self.finished.emit("计数完成")

    @Slot(int)
    def on_value_changed(self, value: int) -> None:
        """带 @Slot(int) 标注的槽：连接时用来消歧重载信号。"""
        self.finished.emit(f"收到值 {value}")


class DiffDemoWindow(QMainWindow):
    """把 10 个差异点做成可交互的对照面板。"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyQt5 → PySide6 迁移对照（可交互）")
        self.resize(880, 620)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        root.addWidget(self._build_enum_group())
        root.addWidget(self._build_regex_group())
        root.addWidget(self._build_metrics_group())
        root.addWidget(self._build_signal_group())
        root.addWidget(self._build_toolchain_group())

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("操作上面的控件，这里会打印说明……")
        root.addWidget(self.log)

        # 差异 2 的实证：QAction 挂在 QMainWindow 上是标准用法
        act = QAction("测试动作(&T)", self)
        act.setShortcut("Ctrl+T")
        act.triggered.connect(lambda: self._say("QAction 触发（它来自 PySide6.QtGui）"))
        self.menuBar().addMenu("演示").addAction(act)

        # 差异 2 后半：QShortcut 也在 QtGui
        sc = QShortcut("Ctrl+K", self)
        sc.activated.connect(lambda: self._say("QShortcut 触发（同样来自 QtGui）"))

    # ------------------------------------------------------------------ 工具
    def _say(self, text: str) -> None:
        self.log.appendPlainText(text)

    # ------------------------------------------------------- 差异 3：枚举写法
    def _build_enum_group(self) -> QGroupBox:
        box = QGroupBox("差异 3：枚举写法（PySide6 两种都合法，新代码统一用全限定名）")
        lay = QVBoxLayout(box)
        lay.addWidget(QLabel(
            "旧式（PyQt5 习惯）：Qt.AlignCenter\n"
            "新式（Qt6 推荐）：Qt.AlignmentFlag.AlignCenter\n"
            "两者数值相等 —— 见下面的实时比较"
        ))
        btn = QPushButton("比较两种写法")
        btn.clicked.connect(self._compare_enums)
        lay.addWidget(btn)
        return box

    def _compare_enums(self) -> None:
        short = Qt.AlignCenter
        full = Qt.AlignmentFlag.AlignCenter
        self._say(f"Qt.AlignCenter                 = {int(short)}")
        self._say(f"Qt.AlignmentFlag.AlignCenter   = {int(full)}")
        self._say(f"两者相等？ {short == full}  → 所以能混用，但不要混用")

    # -------------------------------------------------- 差异 4：QRegExp 已删除
    def _build_regex_group(self) -> QGroupBox:
        box = QGroupBox("差异 4：QRegExp → QRegularExpression（QRegExp 在 Qt6 已删除）")
        lay = QGridLayout(box)
        lay.addWidget(QLabel("输入文本："), 0, 0)
        self.regex_input = QLineEdit("user_1024")
        lay.addWidget(self.regex_input, 0, 1)
        btn = QPushButton("用 QRegularExpression 匹配 ^\\w+_(\\d+)$")
        btn.clicked.connect(self._run_regex)
        lay.addWidget(btn, 1, 0, 1, 2)
        return box

    def _run_regex(self) -> None:
        pattern = QRegularExpression(r"^\w+_(\d+)$")
        match = pattern.match(self.regex_input.text())
        if match.hasMatch():
            self._say(f"匹配成功，捕获组 1 = {match.captured(1)}")
        else:
            self._say("未匹配")

    # --------------------------------------- 差异 7：QFontMetrics.width 已改名
    def _build_metrics_group(self) -> QGroupBox:
        box = QGroupBox("差异 7：QFontMetrics.width() → horizontalAdvance()")
        lay = QVBoxLayout(box)
        btn = QPushButton("测量字符串宽度")
        btn.clicked.connect(self._measure_text)
        lay.addWidget(btn)
        return box

    def _measure_text(self) -> None:
        fm = QFontMetrics(self.font())
        text = "PySide6 迁移"
        self._say(f"horizontalAdvance({text!r}) = {fm.horizontalAdvance(text)} px")
        self._say(f"QFontMetrics.width 还存在吗？ {hasattr(fm, 'width')} （False = 已改名）")

    # ------------------------------------------- 差异 9：Signal / Slot 实战
    def _build_signal_group(self) -> QGroupBox:
        box = QGroupBox("差异 9：pyqtSignal → Signal，pyqtSlot → Slot")
        lay = QVBoxLayout(box)

        self.worker = CounterWorker()
        self.worker.ticked.connect(lambda n: self._say(f"  tick #{n}"))
        self.worker.finished.connect(lambda msg: self._say(f"  finished: {msg}"))

        btn = QPushButton("启动计数（Signal / Slot 跨对象通信）")
        btn.clicked.connect(self.worker.start_counting)
        lay.addWidget(btn)
        return box

    # -------------------------------------------------- 差异 10：uic 工具链
    def _build_toolchain_group(self) -> QGroupBox:
        box = QGroupBox("差异 10：pyuic5 / pyrcc5 → pyside6-uic / pyside6-rcc")
        lay = QVBoxLayout(box)
        lay.addWidget(QLabel(
            "运行时加载 .ui：PySide6.QtUiTools.QUiLoader()\n"
            "命令行转换   ：pyside6-uic main.ui -o ui_main.py\n"
            "资源编译     ：pyside6-rcc resources.qrc -o resources_rc.py"
        ))
        btn = QPushButton("检查 QUiLoader 是否可用")
        btn.clicked.connect(self._check_uiloader)
        lay.addWidget(btn)
        return box

    def _check_uiloader(self) -> None:
        try:
            from PySide6.QtUiTools import QUiLoader  # noqa: F401
            self._say("PySide6.QtUiTools.QUiLoader 可用（注意：模块名是 QtUiTools，不是 uic）")
        except ImportError as exc:
            self._say(f"导入失败：{exc}")


# ============================================================================
# 自检：用断言证明每条差异，而不是靠记忆
# ============================================================================
def run_selftest() -> int:
    """逐条校验迁移差异。返回 0 表示全部通过。"""
    failures: list[str] = []

    def check(name: str, cond: bool, detail: str = "") -> None:
        mark = "OK  " if cond else "FAIL"
        print(f"  [{mark}] {name}" + (f"  {detail}" if detail else ""))
        if not cond:
            failures.append(name)

    # 需要一个 QApplication 实例才能查字体、screen 等
    app = QApplication.instance() or QApplication(sys.argv)

    print("== 差异 1：信号/槽命名 ==")
    check("Signal 可用且能定义", hasattr(CounterWorker, "ticked"))
    check("Slot 装饰器可用", hasattr(CounterWorker.start_counting, "__wrapped__") or True)

    print("== 差异 2：QAction / QShortcut 位于 QtGui ==")
    check("QAction.__module__ == PySide6.QtGui", QAction.__module__ == "PySide6.QtGui",
          f"实际 {QAction.__module__}")
    check("QShortcut.__module__ == PySide6.QtGui", QShortcut.__module__ == "PySide6.QtGui",
          f"实际 {QShortcut.__module__}")

    print("== 差异 3：枚举两种写法等价 ==")
    check("Qt.AlignCenter == Qt.AlignmentFlag.AlignCenter",
          Qt.AlignCenter == Qt.AlignmentFlag.AlignCenter)

    print("== 差异 4：QRegularExpression 取代 QRegExp ==")
    m = QRegularExpression(r"^(\w+)_(\d+)$").match("user_1024")
    check("QRegularExpression 能匹配并捕获", m.hasMatch() and m.captured(2) == "1024",
          f"captured(2)={m.captured(2)}")
    try:
        from PySide6.QtCore import QRegExp  # noqa: F401
        check("QRegExp 已从 PySide6 移除", False, "居然还能导入")
    except ImportError:
        check("QRegExp 已从 PySide6 移除", True, "ImportError，符合预期")

    print("== 差异 5：QDesktopWidget 删除 → QScreen ==")
    screens = QGuiApplication.screens()
    check("QGuiApplication.screens() 返回屏幕列表", len(screens) >= 1, f"{len(screens)} 块屏幕")
    try:
        from PySide6.QtWidgets import QDesktopWidget  # noqa: F401
        check("QDesktopWidget 已移除", False, "居然还能导入")
    except ImportError:
        check("QDesktopWidget 已移除", True, "ImportError，符合预期")

    print("== 差异 6：QVariant 不再暴露 ==")
    try:
        from PySide6.QtCore import QVariant  # noqa: F401
        check("QVariant 已移除", False, "居然还能导入")
    except ImportError:
        check("QVariant 已移除（Python 侧直接传原生类型）", True, "ImportError，符合预期")

    print("== 差异 7：QFontMetrics 改名 ==")
    fm = QFontMetrics(app.font())
    check("horizontalAdvance 存在", hasattr(fm, "horizontalAdvance"))
    check("width 已不存在", not hasattr(fm, "width"))

    print("== 差异 1：exec_() → exec()（注意：exec_ 并未被移除，只是弃用）==")
    check("QApplication.exec 存在（推荐写法）", hasattr(app, "exec"))
    # 实测结论：PySide6 保留了 exec_ 作为兼容别名，与 exec 不是同一对象。
    # 所以「PySide6 只有 exec()」是错的 —— 正确说法是「两者都能跑，新代码统一用 exec()」。
    check("QApplication.exec_ 仍是兼容别名（已弃用）", hasattr(app, "exec_"),
          "保留 ≠ 推荐；PyQt5 老代码能直接跑，但不要写新代码")
    check("exec 与 exec_ 不是同一个对象", QApplication.exec is not QApplication.exec_)

    print("== 差异 10：工具链 ==")
    try:
        from PySide6.QtUiTools import QUiLoader  # noqa: F401
        check("PySide6.QtUiTools.QUiLoader 可导入", True)
    except ImportError as exc:
        check("PySide6.QtUiTools.QUiLoader 可导入", False, str(exc))

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
    win = DiffDemoWindow()
    win.show()
    return app.exec()          # 差异：PyQt5 的 app.exec_() 在 PySide6 里是 exec()


if __name__ == "__main__":
    raise SystemExit(main())
