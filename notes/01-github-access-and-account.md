# 01 · GitHub 登录问题：诊断结论与操作单

> 记录时间：2026-10-02
> 触发报错：`This account does not support password sign-in, please try another sign-in method or account recovery.`

---

## 一、报错到底是什么意思

这句话是 **GitHub 服务端返回的**，所以两件事可以立刻排除：

- **不是你密码输错了** —— 密码错了报的是 `Incorrect username or password`。
- **不是网络问题** —— 网络断了根本收不到这条错误，页面会直接超时。

它的准确含义是：**账号存在，但这个账号没有密码，或已关闭密码登录方式。**
GitHub 近年在推无密码登录（passkey / 第三方账号登录），这类账号在密码框里输任何内容都会被拒。

---

## 二、已查证的账号现状

通过 GitHub 公开 API（`api.github.com`，实测 4/4 稳定）反查 `fxdzlfxdzl` 关键词，命中的账号：

| 字段 | 值 |
|---|---|
| login | **`fxdzlfxdzl-star`** |
| 主页 | https://github.com/fxdzlfxdzl-star |
| 创建时间 | **2026-09-10**（三周前） |
| 公开仓库 | **0** |
| Followers / Following | 0 / 0 |
| 最后更新 | 与创建时间相同（从未改过资料） |

> 邮箱前缀完全一致，**高度疑似**就是你的账号（`-star` 后缀是注册时重名被自动追加的）。
> 如果这不是你的账号，说明你用的邮箱与注册邮箱不一致，下面的分支判断需要相应调整。

**这个结论很关键：账号是个空号。** 里面没有任何提交、任何仓库。所以无论最后选择"找回"还是"重建"，**都不会损失已有内容**，决策成本极低。

---

## 三、三层障碍（全部实测，非推测）

| 层 | 障碍 | 实测数据 | 影响 |
|---|---|---|---|
| ① 账号 | 不支持密码登录 | 服务端明确报错 | 密码这条路直接封死 |
| ② 邮箱 | **Gmail 在本机完全不通** | `accounts.google.com` / `mail.google.com` / `gmail.com` / `www.google.com` 四个端点**全部超时**；TCP 443 握手不通 | 找回邮件收不到 → 重置密码流程走不完 |
| ③ 网页 | **github.com 主站间歇性不可达** | 默认解析到的 `20.205.243.166` 仅 **1/4 ~ 2/4** 成功；`4.237.22.38` 与 `140.82.112.3` 实测 **4/4** 成功 | 登录 / 加公钥 / 建仓库都可能中途断掉 |

### 三个补充事实

- **DNS 没有被污染。** `github.com` 解析到的是 `20.205.243.166`（GitHub 真实 IP），`accounts.google.com` 解析到 `108.177.98.84`（Google 真实 IP）。所以问题是 **IP 级阻断**，不是 DNS 劫持。
- **换 IP 能显著改善。** 同一个域名、同样的 TLS 握手，只是把目标 IP 换成 `4.237.22.38`，成功率就从 1/4 变成 4/4。这证明被拦的是**具体 IP**，不是域名本身。
- **推送通道一直是好的。** `ssh.github.com:443` 连续多次握手成功（返回 `Permission denied (publickey)` 表示握手完成、仅缺公钥）。**也就是说：一旦账号问题解决、公钥配上，`git push` 不会受阻。**
- 国内站点对照正常：`baidu.com` 200 / 3.3s，`gitee.com` 200 / 1.6s。**本机网络本身没问题。**

---

## 四、操作分支（按顺序判断）

### 分支 A —— 能收到 `fxdzlfxdzl@gmail.com` 的邮件

只要你在**任何设备**上能打开这个 Gmail（手机流量、手机上的邮箱 App、反正任何途径），走这条：

1. 打开 https://github.com/password_reset
2. 输入 `fxdzlfxdzl@gmail.com`，点 `Send password reset email`
3. 去 Gmail 收信（**链接 3 小时内有效**，检查垃圾邮件箱）
4. 点开链接 → 设置一个新密码 → 提交

设置成功后，这个账号就有了密码，**以后就能用密码登录了**，今天的报错不会再出现。

> 如果重置页面要求 2FA 验证（弹 passkey / 验证器 / 恢复码），说明账号开过两步验证。用你当时配的方式验证；都没有就转分支 B。

### 分支 B —— 收不到 Gmail（本机确实不通）

那这个账号基本救不回来（GitHub 的找回逻辑强依赖主邮箱）。**直接新建一个账号，代价为零**——旧账号本来就是空的。

1. 打开 https://github.com/signup
2. **用一个国内能正常收信的邮箱**（QQ 邮箱 / 163 邮箱）。这一步很重要：以后所有验证邮件、找回邮件都能立刻收到，不会再卡在 Google 上。
3. **注册时就把密码设好**，不要选"用 Google 账号注册"——那正是今天这个坑的成因。
4. 注册后立刻做两件事：
   - 绑定一个**手机上的验证器 App**（Microsoft Authenticator / Google Authenticator）做两步验证
   - 不要把登录方式设成"仅 passkey"，否则换设备会再次锁死
5. 登录后把 `fxdzlfxdzl@gmail.com` 作为**备用邮箱**加进去并验证（`Settings → Emails → Add email address`）。这样即便你以前用这个邮箱提交过代码，贡献图也能关联上。

> 新建账号后，本地 git 的邮箱要跟着改（见第六节），否则提交不会算进新账号的贡献图。

### 分支 C —— 两条路都想先放一放

也可以先用 **Gitee**（`gitee.com` 实测 200 / 1.6s，SSH 22 端口通，全链路在你电脑上都能走）。它是国内平台，网页、注册、建仓库全部无需任何特殊网络。代价是求职时的分量不如 GitHub。上面两个分支都试过之后再来考虑这条。

---

## 五、修掉 github.com 网页的抽风问题（推荐做）

不改任何东西也能用，只是要反复刷新（成功率 1/4）。改 hosts 后成功率接近 100%，**建议做**。

**方法：双击运行 `F:\workbuddy_work\tools\fix-github-hosts.cmd`**，在弹出的 UAC 对话框点"是"。它会：

1. 再次实测两个候选 IP 的连通性（避免写入已失效的地址）
2. 备份原 hosts 到 `tools\hosts-backup\`
3. 把 `github.com` / `www.github.com` 指向实测通过的 IP
4. 刷新 DNS 缓存

跑完**完全关闭并重开浏览器**再试。

**如果哪天又打不开了**，说明 IP 变了——重跑一次上面那个脚本即可（不传参数时它会重新采样全部候选 IP，约 2 分钟）。

**想恢复原状**：

```powershell
& "C:\Users\zy\.workbuddy\binaries\python\versions\3.13.12\python.exe" "F:\workbuddy_work\tools\github-hosts-fixer.py" --revert
```

**备选方案（不用改 hosts）**：用**手机开热点**让电脑联网。移动网络对 GitHub 的干扰通常比宽带轻，这是零配置的一条路。

---

## 六、账号搞定之后：把本地代码推上去

### ① 添加 SSH 公钥

复制这一整行（这是**公钥**，公开无风险）：

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK2BhnnFMgHac859CmMMQAKogK4Sl5dPcCM5lKe77pHk fxdzlfxdzl@gmail.com
```

GitHub → 右上角头像 → `Settings` → 左侧 `SSH and GPG keys` → `New SSH key` → Title 随意 → 粘贴 → `Add SSH key`。

验证（新终端里跑）：

```bash
ssh -T git@github.com
```

看到 `Hi <用户名>! You've successfully authenticated...` 即成。

### ② 建一个空仓库

右上角 `+` → `New repository`。

⚠️ 三个初始化选项 **全部不要勾**（`Add a README file` / `Add .gitignore` / `Choose a license`）——本地已有这些文件，勾了会造成冲突。

仓库名建议用中性技术名而不是 `learning`，例如 `pyside6-toolbox`。

### ③ 关联并推送

把 `<用户名>` 换成你的 GitHub 登录名（不是 `zhongyu`，那是提交署名）：

```bash
cd /f/workbuddy_work/pyside6-learning
git remote add origin git@github.com:<用户名>/pyside6-toolbox.git
git push -u origin main
```

### ④ 如果建了新账号，改一下提交署名邮箱

```bash
git config --global user.email "你的新邮箱"
git commit --amend --reset-author --no-edit
```

---

## 七、当前本地仓库状态（已就绪，只差远端）

```
仓库        F:\workbuddy_work\pyside6-learning\.git
首次提交    44fc3b3   5 files changed, 357 insertions(+)
跟踪文件    .gitignore  README.md  examples/01_hello_window.py
            notes/00-learning-path.md  requirements.txt
工作区      clean
远端        —— 尚未配置
```

`.venv` 已确认未被跟踪（660MB，一旦误提交仓库就废了）。

---

## 附：本次用到的诊断命令（可复用）

```bash
# GitHub 主站可达性
curl -sS --noproxy '*' -o /dev/null -w "HTTP %{http_code}  %{time_total}s\n" --max-time 8 https://github.com/

# 换 IP 直连，判断是 IP 级还是域名级阻断
curl -sS --noproxy '*' --resolve github.com:443:4.237.22.38 \
     -o /dev/null -w "HTTP %{http_code}  %{time_total}s\n" --max-time 8 https://github.com/

# 推送通道（SSH over 443）
ssh -T git@github.com

# 查任意 GitHub 账号的公开资料
curl -sS https://api.github.com/users/<用户名>
```
