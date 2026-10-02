"""Designer 工作流 · 两条路线对比

第 1 周的产出物骨架。`.ui` 文件在 `ui/main.ui`，用 `pyside6-designer` 可以直接改。

用法::

    python examples/03_designer_workflow.py              # 路线 A：编译式（推荐，默认）
    python examples/03_designer_workflow.py --runtime    # 路线 B：运行时加载 .ui
    python examples/03_designer_workflow.py --selftest   # 自检，不开窗口

两条路线的取舍
--------------
路线 A（pyside6-uic 编译）：
    .ui → ui_main.py → import
    优点：类型提示完整、能被 IDE 索引、启动快、可提交进 git 做 diff
    缺点：改完 .ui 必须重新编译（可配 PyCharm 的 File Watcher 自动化）
    实际项目主流选择。

路线 B（QUiLoader 运行时加载）：
    .ui 随程序分发，运行时解析
    优点：不用编译，改完直接生效
    缺点：子控件只能用 findChild 取，没有 IDE 补全，.ui 语法错误要到运行时才炸
    适合：插件式界面、需要让用户自定义 UI 的工具

⚠️ 与 PyQt5 的差异：PyQt5 有个 `uic.loadUi()` 辅助函数，加载后子控件会直接变成
   对象的 Python 属性（`self.nameEdit`）。**PySide6 没有这个函数**，只有
   `QUiLoader().load()`，子控件必须走 `findChild()`。这是迁移时容易卡住的一处。
"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QWidget

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UI_FILE = PROJECT_ROOT / "ui" / "main.ui"
UI_PY_DIR = PROJECT_ROOT / "ui"


def _greeting_text(name: str) -> str:
    """纯函数：输入昵称 → 输出问候语。便于单测，不碰 UI。"""
    name = name.strip()
    if not name:
        return "你还没输入昵称。"
    return f"你好，{name}！这条消息由 Python 逻辑生成，界面来自 ui/main.ui。"


# ============================================================================
# 路线 A：编译式
# ============================================================================
def build_window_compiled() -> QWidget:
    """用 pyside6-uic 生成的 ui_main.py 构建窗口。"""
    if str(UI_PY_DIR) not in sys.path:
        sys.path.insert(0, str(UI_PY_DIR))

    try:
        from ui_main import Ui_GreeterWindow
    except ImportError as exc:
        raise SystemExit(
            f"找不到 ui/ui_main.py —— 先执行：\n"
            f"    pyside6-uic ui/main.ui -o ui/ui_main.py\n原始错误：{exc}"
        ) from exc

    window = QWidget()
    ui = Ui_GreeterWindow()
    ui.setupUi(window)

    # 手动连线。也可以用 connectSlotsByName 的命名约定：
    # 定义 on_<对象名>_<信号名>() 方法即可自动连接（生成的代码末尾已调用它）。
    def greet() -> None:
        ui.outputLabel.setText(_greeting_text(ui.nameEdit.text()))

    ui.greetButton.clicked.connect(greet)
    ui.nameEdit.returnPressed.connect(greet)      # 回车也能触发
    return window


# ============================================================================
# 路线 B：运行时加载
# ============================================================================
def build_window_runtime() -> QWidget:
    """用 QUiLoader 在运行时解析 ui/main.ui。"""
    from PySide6.QtUiTools import QUiLoader   # 注意模块名是 QtUiTools

    if not UI_FILE.exists():
        raise SystemExit(f"找不到 {UI_FILE}")

    # QUiLoader 要求先有 QApplication 实例
    loader = QUiLoader()
    window = loader.load(str(UI_FILE))
    if window is None:
        raise SystemExit(f"加载失败：{UI_FILE}")

    # 与 PyQt5 的 uic.loadUi 不同，子控件不是属性，必须 findChild
    name_edit = window.findChild(QLineEdit, "nameEdit")
    output_label = window.findChild(QWidget, "outputLabel")
    button = window.findChild(QPushButton, "greetButton")

    missing = [n for n, o in
               (("nameEdit", name_edit), ("outputLabel", output_label), ("greetButton", button))
               if o is None]
    if missing:
        raise SystemExit(f".ui 里缺少控件：{missing}")

    def greet() -> None:
        output_label.setText(_greeting_text(name_edit.text()))

    button.clicked.connect(greet)
    name_edit.returnPressed.connect(greet)
    return window


# ============================================================================
# 自检
# ============================================================================
def run_selftest() -> int:
    failures: list[str] = []

    def check(name: str, cond: bool, detail: str = "") -> None:
        print(f"  [{'OK  ' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
        if not cond:
            failures.append(name)

    app = QApplication.instance() or QApplication(sys.argv)   # noqa: F841

    print("== 纯逻辑（不依赖 UI）==")
    check("空输入返回提示", _greeting_text("  ") == "你还没输入昵称。")
    check("正常输入生成问候", _greeting_text(" 阿宇 ") ==
          "你好，阿宇！这条消息由 Python 逻辑生成，界面来自 ui/main.ui。")

    print("== 文件就位 ==")
    check("ui/main.ui 存在", UI_FILE.exists(), str(UI_FILE.relative_to(PROJECT_ROOT)))
    check("ui/ui_main.py 存在", (UI_PY_DIR / "ui_main.py").exists())

    print("== 路线 A：编译式 ==")
    try:
        w = build_window_compiled()
        check("构建窗口成功", w is not None)
        btn = w.findChild(QPushButton, "greetButton")
        edit = w.findChild(QLineEdit, "nameEdit")
        out = w.findChild(QWidget, "outputLabel")
        check("控件对象名可查", all(x is not None for x in (btn, edit, out)))
        edit.setText("测试")
        btn.click()
        check("点击按钮更新输出",
              out.text() == _greeting_text("测试"), out.text())
    except SystemExit as exc:
        check("构建窗口成功", False, str(exc))

    print("== 路线 B：运行时加载 ==")
    try:
        w2 = build_window_runtime()
        check("QUiLoader 加载成功", w2 is not None)
        btn2 = w2.findChild(QPushButton, "greetButton")
        edit2 = w2.findChild(QLineEdit, "nameEdit")
        out2 = w2.findChild(QWidget, "outputLabel")
        edit2.setText("运行时")
        btn2.click()
        check("点击按钮更新输出",
              out2.text() == _greeting_text("运行时"), out2.text())
    except SystemExit as exc:
        check("QUiLoader 加载成功", False, str(exc))

    print("== 迁移知识点：PyQt5 的 uic.loadUi 在 PySide6 不存在 ==")
    try:
        from PySide6 import uic as _uic
        check("PySide6.uic 模块不存在", False, "居然存在")
    except ImportError:
        check("PySide6.uic 模块不存在", True, "改用 QtUiTools.QUiLoader")

    print()
    if failures:
        print(f"结果：{len(failures)} 项未通过 -> {failures}")
        return 1
    print("结果：全部通过")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if "--selftest" in argv:
        return run_selftest()

    app = QApplication(sys.argv)
    window = build_window_runtime() if "--runtime" in argv else build_window_compiled()
    mode = "路线 B（运行时 QUiLoader）" if "--runtime" in argv else "路线 A（编译式 uic）"
    window.setWindowTitle(f"{mode} · {window.windowTitle()}")
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
