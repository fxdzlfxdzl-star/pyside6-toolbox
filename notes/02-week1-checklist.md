# 第 1 周执行清单 · 找回手感 + 吃透差异

> 目标产出：**一个能用 Designer 改的 `.ui` + `.py` 组合项目**
> 骨架已经给你搭好了（`ui/main.ui` + `ui/ui_main.py` + `examples/03_designer_workflow.py`），
> 你要做的是把它改成自己的东西，而不是从零抄。

---

## Day 1（约 1 小时）· 环境确认 + 跑通示例

这一步不写代码，只确认"手是热的"。

- [ ] **重启 PyCharm**（之前启动时系统还没有 git，要重启才能识别）
- [ ] `Open` → `F:\workbuddy_work\pyside6-learning`
- [ ] 右下角确认解释器显示 `Python 3.12 (pyside6-learning)`；不是的话：
      `Settings` → `Project` → `Python Interpreter` → 齿轮 → `Add Local Interpreter` →
      `Existing` → 选 `.venv\Scripts\python.exe`
- [ ] 依次运行（右键 → Run）：
      - `examples/01_hello_window.py` → 弹出 Hello 窗口
      - `examples/02_migration_diffs.py` → 弹出对照窗口，点几下按钮看日志
      - `examples/03_designer_workflow.py` → 弹出问候窗口，输入文字点按钮

**验收**：三个窗口都能弹出，无红色报错。

命令行方式（PyCharm 的 Terminal 里，venv 会自动激活）：

```bash
python examples/02_migration_diffs.py --selftest
python examples/03_designer_workflow.py --selftest
```

两条都应打印「结果：全部通过」并以退出码 0 结束。

> 如果你在 WorkBuddy 的 shell 里跑，需要加 `env -u PYTHONPATH` 前缀（原因见
> `notes/01-github-access-and-account.md`）。在 PyCharm 自带的 Terminal 里不需要。

---

## Day 2（约 3 小时）· 吃透 10 个差异

**不要看文档抄。** 先自己默写，再对答案 —— 这一步的目的是暴露你记忆里的错误。

- [ ] 关掉 `notes/00-learning-path.md` 的 1.2 节，自己写出 10 条差异
- [ ] 写完后逐条对照，把写错的用红笔（或注释）标出来
- [ ] 每条差异各写一个**最小可运行示例**（10~30 行即可），放 `examples/diffs/` 下，命名 `d01_exec.py` ... `d10_uic.py`
- [ ] 每条都能 `python examples/diffs/dNN_xxx.py` 跑出结果

**验收**：10 个文件存在且都能跑；你能不查资料说出每条差异的**原因**（不只是"名字变了"）。

已有的两条实测结论值得注意（都是这次验证出来的）：

| 容易记错的说法 | 实测真相 |
|---|---|
| "PySide6 把 `exec_()` 删了" | **没删**，保留为兼容别名，只是弃用。说"删了"会被面试官抓 |
| "`QRegExp` 还能用，只是慢" | **已彻底移除**，import 直接 ImportError |

---

## Day 3（约 3 小时）· Designer 全流程打通

- [ ] 命令行启动 Designer（**必须用 venv 里的那个**，系统里没有）：

```bash
.venv\Scripts\pyside6-designer.exe ui/main.ui
```

- [ ] 随便改点东西：加一个 `QCheckBox`、改个文字、调一下间距
- [ ] 保存，回到 PyCharm 重新编译：

```bash
.venv\Scripts\pyside6-uic.exe ui/main.ui -o ui/ui_main.py
```

- [ ] 再跑 `examples/03_designer_workflow.py`，确认看到你改的效果
- [ ] **配自动编译**（省掉每次手敲）：
      `Settings` → `Tools` → `File Watchers` → `+` → `Custom`
      - Name: `pyside6-uic`
      - File type: `Qt UI Designer Form`
      - Program: `$ProjectFileDir$\.venv\Scripts\pyside6-uic.exe`
      - Arguments: `$FilePath$ -o $FileDir$/ui_$FileNameWithoutExtension$.py`
      - Working directory: `$FileDir$`

**验收**：改 `.ui` 保存后，`ui_main.py` 自动更新，运行程序看到变化。

> 概念澄清：`pyside6-designer` 只是个**画界面的工具**，不参与程序运行。
> 程序运行时要么读编译好的 `.py`（路线 A），要么运行时解析 `.ui`（路线 B）——
> 两条路线见 `examples/03_designer_workflow.py` 的文档字符串。

---

## Day 4（约 4 小时）· 重写一个你以前做过的界面

**这是本周唯一真正的"产出"，前面三天都是为它服务。**

- [ ] 挑一个以前用 PyQt 做过的界面 —— **越熟悉越好**，不要挑新的
- [ ] 新建 `examples/my_first_port/`，用 PySide6 重写一遍
- [ ] 刻意用上：`Signal` / `Slot`、布局管理器（**不许用绝对坐标**）、至少一个自定义控件
- [ ] 顺手记下"哪里卡住了" —— 这些卡点就是你两年空窗真正的知识缺口

**验收**：新写的版本能跑，并且你能说清楚"和当年 PyQt 版相比改了什么"。

> 挑熟悉界面的原因：你不需要同时思考"这个功能该怎么做"和"这个 API 叫什么"。
> 变量只有一个，才能准确测量出你到底缺哪块。

---

## Day 5（约 2 小时）· 整理 + 提交

- [ ] 把 Day 2 的 10 个示例和 Day 4 的项目补上简短注释
- [ ] 更新 `README.md`，说明这个仓库现在装了什么
- [ ] 提交并推送：

```bash
git add -A
git commit -m "Week 1: PyQt5 to PySide6 migration reference and Designer workflow"
git push
```

**验收**：GitHub 上能看到这次提交；贡献图出现今天的格子。

---

## 每周固定的 git 节奏

从这周开始养成习惯 —— 这直接服务于你两年空窗的补救：

- **每天至少一次提交**，哪怕只是"补了个注释"。原因：面试官看的是**连续**的提交记录，
  不是某天写了 500 行。空白期比低强度更可疑。
- 提交信息写清楚做了什么，不要 `update` / `fix` 这种。
- 每周结束时 `git push`，本地提交不算数。

---

## 本周常见坑（先看一遍，省得卡住）

| 现象 | 原因 | 解决 |
|---|---|---|
| PyCharm 运行时报 `ModuleNotFoundError: PySide6` | 解释器指向了系统 Python 而不是 `.venv` | 检查右下角解释器 |
| `pyside6-designer` 命令找不到 | venv 没激活，或用了系统 shell | 用完整路径 `.venv\Scripts\pyside6-designer.exe` |
| 改了 `.ui` 但程序没变化 | 忘了重新编译 | 配 File Watcher（见 Day 3） |
| `ModuleNotFoundError: ui_main` | `ui/` 不在 `sys.path` | 参考 `examples/03_designer_workflow.py` 里 `sys.path.insert` 的写法 |
| pip 安装报 `SystemExit: 1` | WorkBuddy 注入的 `PYTHONPATH` 拦截 | 命令前加 `env -u PYTHONPATH`（PyCharm Terminal 里不会遇到） |

---

## 关于 `ui/ui_main.py` 要不要提交进 git

**建议提交。** 理由：别人 clone 下来能直接跑，不用先装 `pyside6-uic` 走一遍编译。
文件头那行 `WARNING! All changes made in this file will be lost when recompiling` 是提示
你别手改这个文件（要改去改 `.ui`），不是叫你别提交。

另一派做法是 gitignore 掉、构建时生成 —— 团队协作里更常见。你现在是个人作品集，
选"能直接跑"的那条更划算。
