# PySide6 求职学习路线

> 适用对象：有 PyQt 实战经验、空窗两年、目标重返"客户端/工具开发"岗位。
> 核心判断：**你不缺 Qt 知识，缺的是"版本迭代落差 + 手感 + 现在的工程规范"。**

---

## 0. 先想清楚：为什么是 PySide6 而不是 PyQt

这是面试里会问的第一个问题，答案要能脱口而出：

| 维度 | PyQt6 | PySide6 |
|---|---|---|
| 维护方 | Riverbank（第三方） | Qt 官方（The Qt Company） |
| 许可证 | GPL v3 / 商业授权 | LGPL v3 / 商业授权 |
| 商业闭源 | GPL 下必须开源，否则买商业授权（贵） | LGPL 下可动态链接闭源发布 |
| API 风格 | 强制新式枚举，命名更"严格" | 兼容旧式写法，迁移成本低 |
| 官方工具链 | 社区维护 | 官方 pyside6-uic / rcc / deploy |

**结论**：商业项目、游戏公司工具链几乎一边倒选 PySide6，就是因为 LGPL。这也是你简历上应该写 PySide6 的理由。

---

## 1. PyQt → PySide6 迁移对照表（第一周主力内容）

这部分你两天就能刷完，但必须手写一遍，形成肌肉记忆。

### 1.1 模块与命名

| 用途 | PyQt5 | PySide6 |
|---|---|---|
| 主模块 | `PyQt5.QtWidgets` | `PySide6.QtWidgets` |
| 信号定义 | `pyqtSignal` | `Signal` |
| 槽装饰器 | `pyqtSlot` | `Slot` |
| 属性 | `pyqtProperty` | `Property` |
| 绑定机制 | SIP | Shiboken |

```python
# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class Worker(QObject):
    finished = pyqtSignal(int)

    @pyqtSlot()
    def run(self):
        self.finished.emit(42)

# PySide6
from PySide6.QtCore import Signal, Slot, QObject

class Worker(QObject):
    finished = Signal(int)

    @Slot()
    def run(self):
        self.finished.emit(42)
```

### 1.2 最容易被坑的 10 个点

> 以下每条都用 `examples/02_migration_diffs.py --selftest` 实测校验过（PySide6 6.11.2 / Python 3.12.10）。
> 结论标注：[已移除] = import 直接报错；[仅弃用] = 还能跑但不该写新代码。

1. **`exec_()` → `exec()`【仅弃用，非移除】**：PySide6 **保留了 `exec_` 作为兼容别名**（与 `exec` 不是同一个对象），PyQt5 老代码能直接跑。但新代码一律写 `app.exec()` / `dialog.exec()` —— 面试时说"exec_ 被移除了"会被抓。
2. **`QAction` / `QShortcut` 从 QtWidgets 搬到 QtGui**【已实测确认】。这是 Qt6 层面的改动，PyQt6 也一样。
3. **枚举写法**：PySide6 两种都能用（`Qt.AlignCenter` 与 `Qt.AlignmentFlag.AlignCenter` **数值相等**），但**写新代码一律用全限定名**，面试时更专业。
4. **`QRegExp` → `QRegularExpression`**【已移除】，import 直接 ImportError。
5. **`QDesktopWidget` → `QScreen` / `QGuiApplication.screens()`**【已移除】。
6. **`QVariant`**【已移除】，Python 侧直接传原生类型。
7. **`QFontMetrics.width()` → `horizontalAdvance()`**【已移除】，`hasattr(fm, 'width')` 为 False。
8. **`unicode` 相关 API 全部消失**，Python 3 只有 `str`。
9. **信号重载**写法变了：`Signal(int)` 定义，连接时靠参数签名或 `@Slot(int)` 区分。
10. **`uic` 模块路径变了**：`PySide6.QtUiTools` + `QUiLoader`；命令行是 `pyside6-uic`。

### 1.3 官方工具链（替代 PyQt 的 pyrcc5 / pyuic5）

```bash
pyside6-designer                      # 打开 Qt Designer
pyside6-uic main.ui -o ui_main.py     # .ui → .py
pyside6-rcc resources.qrc -o resources_rc.py   # 资源编译
pyside6-deploy                        # Nuitka 打包（官方）
pyside6-lupdate / pyside6-lrelease    # 国际化
```

---

## 2. 六周计划（每周 5 天 × 3~5 小时）

### 第 1 周：找回手感 + 吃透差异
- [ ] 跑 `examples/02_migration_diffs.py`（窗口模式 + `--selftest` 模式各跑一遍）。
- [ ] 逐条对照 `notes/02-week1-checklist.md`，把 10 个差异点各写一个自己的最小示例。
- [ ] 用 PySide6 重写一个你以前做过的 PyQt 界面（哪怕简单）。
- [ ] 熟悉 `pyside6-designer` + `pyside6-uic` 的完整流程。
- **产出**：一个能用 Designer 改的 `.ui` + `.py` 组合项目。
- **详细任务拆解见 `notes/02-week1-checklist.md`。**

### 第 2 周：Qt 核心机制补课（面试重灾区）
- [ ] **信号槽底层**：直连 / 队列连接 / 自动连接的差异，跨线程为什么必须 QueuedConnection。
- [ ] **事件循环与事件过滤**：`QEvent`、`installEventFilter`、`event()` 重写。
- [ ] **QThread 三种用法**：继承 QThread、moveToThread（**推荐**）、QThreadPool + QRunnable。
- [ ] **进程与线程安全**：为什么子线程不能碰 UI，`QMetaObject.invokeMethod` 怎么用。
- **产出**：一个后台线程跑耗时任务、UI 不卡死、带进度条和取消按钮的 Demo。

### 第 3 周：Model/View 与数据层
- [ ] `QAbstractItemModel` 自定义模型（面试高频，能写出来就赢一半）。
- [ ] `QSortFilterProxyModel` 做搜索过滤。
- [ ] `QTableView` / `QListView` / `QTreeView` 的 `setModel` 与 delegate 自定义绘制。
- [ ] `QSettings` 存配置，SQLite（`sqlite3` 或 `QtSql`）存业务数据。
- **产出**：一个树形 + 表格的"资源管理器"式界面。

### 第 4 周：界面工程化 + 定制外观
- [ ] QSS 样式表：选择器、伪状态、和 CSS 的差异。
- [ ] 自定义控件：继承 `QWidget` 自己画（`paintEvent` + `QPainter`）。
- [ ] 无边框窗口、自定义标题栏、拖拽、`QGraphicsView` 入门。
- [ ] 多语言（`.ts` 文件 + `QTranslator`）。
- **产出**：一套自己的"暗色主题" QSS + 一个自定义标题栏窗口。

### 第 5 周：打包、测试、部署
- [ ] `PyInstaller` 打包 PySide6（含图标、资源、单文件 vs 目录模式的坑）。
- [ ] `pyside6-deploy`（Nuitka）对比，知道各自体积和启动速度差异。
- [ ] `pytest` + `pytest-qt`：怎么测信号、怎么模拟点击。
- [ ] 日志（`logging`）+ 全局异常捕获（`sys.excepthook` + `QMessageBox`）。
- **产出**：一个能双击运行的 `.exe`，并且有单元测试。

### 第 6 周：项目 + 简历 + 面试
- [ ] 打磨一个能讲的完整项目（见第 4 节建议）。
- [ ] 补 Python 基本功：装饰器、生成器、`typing`、`dataclass`、GIL、`asyncio` 与 Qt 的关系。
- [ ] 刷算法题（面试门槛，BFS/DFS/DP/字符串）。
- **产出**：简历项目条目 + 3 分钟项目讲解脚本。

---

## 3. 面试高频考点（按出现频率排序）

**Qt / GUI 方向**
1. 信号槽的连接方式有哪几种？跨线程连接为什么不能直连？
2. `moveToThread` 的正确姿势是什么？为什么不能在子线程里 `new QWidget`？
3. `QWidget` 和 `QMainWindow` 的区别，`QMainWindow` 的停靠区/中央区机制。
4. 布局管理器：为什么不要用绝对坐标？`setStretchFactor` / `QSpacerItem` 怎么用？
5. 事件传递流程：`event()` → `notify()` → 事件过滤器。
6. Qt 的父子对象机制与内存管理：什么时候会 double free？`deleteLater()` 为什么存在？
7. `QSS` 和 CSS 的区别，样式不生效的常见原因。
8. 大列表卡顿怎么优化？（Model/View 复用、`setUniformItemSizes`、分页、`QAbstractItemModel` 懒加载）

**Python 基本功**
9. GIL 是什么，为什么 GUI 里还要开线程（答：IO 释放 GIL + 不能让主线程阻塞）。
10. 装饰器原理，手写一个带参数的装饰器。
11. 深浅拷贝、可变默认参数陷阱。
12. `__slots__`、`__new__` vs `__init__`。

**工程素养**
13. 项目怎么组织目录？（MVC / MVVM 分层，UI 与逻辑解耦）
14. 打包后体积大怎么优化？
15. 怎么做版本管理和灰度发布？

---

## 4. 简历项目建议（挑 1~2 个做深，别做多）

针对"游戏工具链"岗位，这几个方向最对味：

| 项目方向 | 技术点覆盖 | 亮点话术 |
|---|---|---|
| 引擎资源打包/导出工具 | 多线程 + Model/View + 进程调用 + 日志 | "把 3000 个资源的导出从 12 分钟优化到 90 秒（线程池 + 批量提交）" |
| 游戏配置表编辑器 | 自定义 Model + 校验 + Excel 导入导出 + Undo/Redo | "用 `QUndoStack` 实现了完整回退，编辑 10 万行不卡" |
| 节点式技能/剧情编辑器 | `QGraphicsView` + 序列化 + 插件机制 | "用 QGraphicsScene 做了 60fps 的节点连线编辑器" |
| 自动化测试面板 / 设备调试上位机 | 串口/网络 + 实时曲线（pyqtgraph）+ 多线程采集 | "采集 1kHz 数据不丢帧，UI 帧率稳定" |

**简历写法**：动作 + 技术 + 量化结果。不要写"使用 PySide6 开发界面"这种废话。

---

## 5. 两年空窗怎么解释

面试必问，提前准备一个**不超过 60 秒**的版本：
- 不编造、不卖惨、不甩锅。
- 结构：客观原因（一句话）→ 这段时间做了什么（哪怕只有一点技术相关）→ 现在为什么回来。
- 把话题往技术上引："这期间我重新系统过了 Qt6 的 model/view 和打包链路。"

**现在就能做的补救**：把 Github 上这段时间的提交补起来。哪怕从现在开始，六周计划做完也有 40+ 天连续提交记录。

---

## 6. 学习方式建议

1. **官方文档优先**：`doc.qt.io/qtforpython-6/`，比任何中文教程都准。
2. **别只看不写**：每个知识点必须有能跑起来的代码，放进 `examples/` 目录。
3. **每周一个可交付物**：见上面每周的"产出"。空窗期求职，作品集比证书管用。
4. **读源码**：`site-packages/PySide6/` 下的 `.pyi` 存根是最好的 API 参考。
5. **控制信息摄入**：教程看一个就够，剩下时间写代码。

---

## 附：常用命令速查

```bash
# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate          # Windows

# 安装
pip install PySide6

# 生成依赖清单
pip freeze > requirements.txt
```
