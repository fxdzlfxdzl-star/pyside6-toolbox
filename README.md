# pyside6-learning

PySide6 学习与求职练习项目。环境已配置完成，直接开工。

## 环境清单

| 组件 | 版本 | 路径 |
|---|---|---|
| Python | 3.12.10 | `C:\Users\zy\AppData\Local\Programs\Python\Python312\python.exe` |
| PySide6 | 6.11.2（含 Essentials + Addons） | 项目虚拟环境内 |
| Qt | 6.11.2 | — |
| IDE | PyCharm Community Edition 2025.2.6.1 | `C:\Program Files\JetBrains\PyCharm Community Edition 2025.2.6.1` |
| 虚拟环境 | venv | `F:\workbuddy_work\pyside6-learning\.venv` |

> 系统里原本的 Python 2.7（`C:\Python27`）已从系统 PATH 中移除（目录保留未删），否则你在新终端敲 `python` 会命中 2.7。

## 第一次打开 PyCharm

1. **启动**：开始菜单 → JetBrains → PyCharm Community Edition 2025.2.6.1
2. **登录**：JetBrains 现在要求用账号激活，即使免费版也一样。注册一个 JetBrains Account（免费），登录后选免费许可即可。跳过 Pro 试用提示。
3. **打开项目**：`Open` → 选择 `F:\workbuddy_work\pyside6-learning`
4. **配置解释器**：PyCharm 通常会自己发现 `.venv` 并提示，直接确认即可。如果没提示：
   - `File` → `Settings` → `Project: pyside6-learning` → `Python Interpreter`
   - 齿轮 → `Add Local Interpreter` → `Existing`
   - 选择 `F:\workbuddy_work\pyside6-learning\.venv\Scripts\python.exe` → OK
5. **跑通第一个例子**：打开 `examples/01_hello_window.py`，右上角点 ▶ Run

成功标志：弹出标题为 `Hello PySide6` 的窗口。

## 命令行方式（可选）

```bash
cd F:\workbuddy_work\pyside6-learning
.venv\Scripts\activate
python examples\01_hello_window.py
```

## 目录结构

```
pyside6-learning/
├── .venv/            # 虚拟环境（不要提交到 git）
├── examples/         # 每个知识点的最小可运行示例
│   ├── 01_hello_window.py          # 最小窗口，验证环境
│   ├── 02_migration_diffs.py       # PyQt5→PySide6 十项差异，可交互对照 + --selftest
│   └── 03_designer_workflow.py     # Designer 两条路线（编译式 / 运行时加载）
├── ui/               # Qt Designer 的 .ui 与编译产物
│   ├── main.ui                     # 用 pyside6-designer 打开改
│   └── ui_main.py                  # pyside6-uic 生成，不要手改
├── notes/            # 学习笔记
│   ├── 00-learning-path.md         # 六周路线 + 迁移对照表 + 面试考点
│   ├── 01-github-access-and-account.md  # 网络与账号排障记录
│   └── 02-week1-checklist.md       # 第 1 周逐日执行清单 ← 从这里开始
└── assets/           # 图标、qrc 资源等
```

## 快速开始

三个示例都能跑，且有自检模式（不开窗口，直接验证 API）：

```bash
python examples/02_migration_diffs.py --selftest
python examples/03_designer_workflow.py --selftest
```

两条都应输出「结果：全部通过」。

**下一步看 `notes/02-week1-checklist.md`**（第 1 周逐日任务）。

## 学习方式

**每个知识点必须落一个能跑的 `examples/` 文件**，不要只读不写。路线见 `notes/00-learning-path.md`。

## 常用命令

```bash
# Qt Designer（可视化拖界面）
.venv\Scripts\pyside6-designer.exe

# .ui 文件转 Python
.venv\Scripts\pyside6-uic.exe main.ui -o ui_main.py

# 资源文件编译
.venv\Scripts\pyside6-rcc.exe resources.qrc -o resources_rc.py

# 导出依赖清单
.venv\Scripts\python.exe -m pip freeze > requirements.txt
```
