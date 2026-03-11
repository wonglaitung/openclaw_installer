# AGENTS.md - OpenClaw 项目文档

## 项目概述

OpenClaw 是一个基于 AI 的智能助手框架，提供命令行界面、Web 界面和系统托盘应用三种交互方式。该项目集成了 Node.js 和 Python 运行环境，支持自定义 AI 模型、技能扩展和多种集成方式，特别适合 Windows 用户进行本地化 AI 助手部署。

### 核心特性

- **多模态交互**：支持命令行、Web 界面和系统托盘应用
- **系统托盘集成**：Windows 原生托盘应用，支持开机自启动和图形化管理，后台运行无干扰
- **动态配置读取**：从用户主目录的配置文件自动读取端口和 token 设置
- **自定义 AI 模型**：集成阿里云 GLM-5 模型（通过自定义提供商）
- **技能系统**：支持扩展技能（港股查询、股票新闻查询）
- **会话管理**：持久化会话历史和配置
- **设备管理**：支持设备配对和多设备访问
- **Shell 集成**：提供多种 Shell 的自动补全支持
- **便捷管理**：一键启动/停止/重启服务，快速访问日志和配置，支持初始化设定
- **代码管理**：支持 Git 版本控制，代码托管在 GitHub

### 技术栈

- **运行环境**：
  - Node.js v22.21.1 (Windows x64)
  - Python 3.12
- **AI 模型**：
  - GLM-5 (通过阿里云 DashScope API)
  - 上下文窗口：16,000 tokens
  - 最大输出：4,096 tokens
- **系统托盘**：
  - pystray (托盘图标管理)
  - Pillow (图像处理)
- **开发工具**：
  - Git (版本控制)
  - GitHub (代码托管)
  - Bash, Fish, PowerShell, Zsh (Shell 支持)

## 项目结构

```
openclaw/
├── .openclaw/                    # 主配置目录（项目内）
│   ├── gateway.cmd               # Gateway 启动脚本
│   ├── openclaw.json             # 主配置文件（备份）
│   └── update-check.json         # 更新检查配置
├── node-v22.21.1-win-x64/        # Node.js 运行环境
│   ├── node.exe
│   ├── npm
│   ├── npx
│   ├── openclaw                  # OpenClaw 核心包
│   └── node_modules/
├── Python312/                    # Python 3.12 运行环境
│   ├── python.exe
│   └── Lib/                      # Python 标准库
├── yfinancenews/                 # Yahoo Finance 新闻查询技能（项目内）
│   ├── SKILL.md                  # 技能文档
│   ├── yfinancenews.skill        # 技能标记文件
│   └── scripts/
│       └── fetch_news.py         # 新闻查询脚本
├── start_openclaw.bat            # 主启动脚本
├── start_tray.bat                # 托盘应用启动脚本
├── install_tray_startup.bat      # 安装开机自启动
├── uninstall_tray_startup.bat    # 卸载开机自启动
├── tray_app.py                   # 托盘应用主程序
├── README.md                     # 项目说明文档
└── AGENTS.md                     # 本文档

~/.openclaw/                      # 用户主目录配置（实际运行时使用）
├── openclaw.json                 # 主配置文件（动态读取）
├── agents/                       # 代理配置
│   └── main/
│       ├── agent/                # 代理配置文件
│       └── sessions/             # 会话历史
├── browser/                      # 浏览器相关配置
├── canvas/                       # 画布功能
├── completions/                  # Shell 自动补全脚本
│   ├── openclaw.bash
│   ├── openclaw.fish
│   ├── openclaw.ps1
│   └── openclaw.zsh
├── cron/                         # 定时任务配置
│   └── jobs.json
├── devices/                      # 设备配对信息
│   ├── paired.json
│   └── pending.json
├── identity/                     # 设备身份标识
│   └── device.json
├── logs/                         # 日志文件
└── workspace/                    # 工作空间
    ├── AGENTS.md                 # 项目文档
    ├── BOOTSTRAP.md              # 初始化引导
    ├── HEARTBEAT.md              # 心跳检查配置
    ├── IDENTITY.md               # AI 身份配置
    ├── MEMORY.md                 # 长期记忆
    ├── SKILL.md                  # 技能说明
    ├── SOUL.md                   # AI 个性配置
    ├── TOOLS.md                  # 工具配置
    ├── USER.md                   # 用户信息
    ├── .git/                     # Git 仓库
    ├── .openclaw/                # 工作空间配置
    └── skills/                   # 技能模块
        ├── aastocks/             # 港股查询技能
        │   ├── SKILL.md
        │   ├── aastocks.skill
        │   └── scripts/
        │       └── fetch_stock.py
        └── yfinancenews/         # Yahoo Finance 新闻查询技能
            ├── SKILL.md
            ├── yfinancenews.skill
            └── scripts/
                └── fetch_news.py
```

## 安装和配置

### 环境要求

- Windows 10/11 或 WSL2
- Node.js v22.21.1（已包含）
- Python 3.12（已包含）

### 首次运行

1. **初始化**：
   ```bash
   start_openclaw.bat onboard
   ```
   或通过托盘应用右键菜单选择"初始化设定"

2. **启动 Gateway**（命令行方式）：
   ```bash
   start_openclaw.bat
   ```
   或
   ```bash
   start_openclaw.bat gateway
   ```

3. **启动托盘应用**（推荐）：
   ```bash
   start_tray.bat
   ```

4. **访问 Web 界面**：
   - 命令行方式：启动后会自动打开浏览器
   - 托盘方式：右键托盘图标选择"打开 Web 界面"
   - 访问地址：`http://localhost:18789`

### 安装系统托盘应用

**启动托盘应用**：
```bash
start_tray.bat
```

**设置开机自启动**：
```bash
install_tray_startup.bat
```

**卸载开机自启动**：
```bash
uninstall_tray_startup.bat
```

### 配置文件

主要配置文件位于 `~/.openclaw/openclaw.json`（用户主目录）：

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "custom-coding-dashscope-aliyuncs-com": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "your-api-key",
        "api": "openai-completions",
        "models": [
          {
            "id": "glm-5",
            "contextWindow": 16000,
            "maxTokens": 4096
          }
        ]
      }
    }
  },
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "your-token"
    }
  }
}
```

**注意**：托盘应用会从此配置文件动态读取端口和 token 设置。

## 使用指南

### 命令行使用

**启动模式**：
```bash
# 默认模式（Gateway + Web）
start_openclaw.bat

# 仅启动 Gateway（不打开网页）
start_openclaw.bat onboard

# Gateway 模式（打开网页）
start_openclaw.bat gateway
```

**直接使用 openclaw 命令**：
```bash
# 确保 PATH 中包含 Node.js 路径
openclaw gateway
openclaw onboard
```

### 系统托盘应用使用（推荐）

**启动托盘应用**：
```bash
start_tray.bat
```

**启动特性**：
- 双击 `start_tray.bat` 后，命令行窗口会快速关闭
- 托盘应用在后台运行，不会显示命令行窗口
- OpenClaw 图标会自动出现在 Windows 系统托盘区（红色圆形图标，显示 "OC"）
- Gateway 服务会自动启动
- 自动从 `~/.openclaw/openclaw.json` 读取配置

启动后，右键点击系统托盘图标可访问以下功能：

- **打开 Web 界面** - 直接在浏览器中打开 OpenClaw 界面
- **初始化设定** - 执行 OpenClaw 初始化配置（onboard 命令）
- **启动服务** - 手动启动 OpenClaw Gateway
- **停止服务** - 停止 OpenClaw Gateway
- **重启服务** - 重启 OpenClaw Gateway
- **查看状态** - 显示当前运行状态（运行中/已停止），并弹出通知
- **打开日志目录** - 打开日志文件夹
- **打开配置文件** - 打开配置文件
- **退出** - 关闭托盘应用和 Gateway

**托盘应用特性**：
- 后台运行，不占用桌面空间
- 自动启动 Gateway 服务
- 实时状态监控（每 5 秒检查一次）
- 一键访问日志和配置
- 支持开机自启动
- 友好的图形界面
- 启动时显示通知
- 动态读取配置文件（端口、token）
- 红色圆形图标，白色 "OC" 文字

### Web 界面使用

1. 启动后访问 `http://localhost:18789`
2. 使用配置的 token 进行认证
3. 开始与 AI 助手对话

### 技能使用

**港股查询技能**：

```bash
cd ~/.openclaw/workspace/skills/aastocks/scripts
python3 fetch_stock.py 01398  # 工商银行
python3 fetch_stock.py 0700   # 腾讯控股
python3 fetch_stock.py 0001   # 长和
```

支持的股票代码格式：
- 5 位数字：`01398`
- 带 HK 前缀：`HK1398`
- 带分隔符：`01398.HK`

**股票新闻查询技能**：

```bash
cd ~/.openclaw/workspace/skills/yfinancenews/scripts
python3 fetch_news.py AAPL        # 苹果公司
python3 fetch_news.py 0700.HK     # 腾讯控股
python3 fetch_news.py MSFT --limit 10  # 微软，返回10条新闻
```

支持的股票代码格式：
- 美股：AAPL, MSFT, TSLA 等
- 港股：1398.HK, 0700.HK 等
- A股（上海）：600519.SS 等
- A股（深圳）：000001.SZ 等

### Shell 自动补全

安装对应的补全脚本：

**Bash**：
```bash
source ~/.openclaw/completions/openclaw.bash
```

**Zsh**：
```bash
source ~/.openclaw/completions/openclaw.zsh
```

**PowerShell**：
```powershell
. "~/.openclaw/completions/openclaw.ps1"
```

## 开发指南

### Git 工作流

项目使用 Git 进行版本控制，代码托管在 GitHub：

**仓库地址**：https://github.com/wonglaitung/openclaw_installer

**基本工作流**：
```bash
# 克隆仓库（如果还没有）
git clone https://github.com/wonglaitung/openclaw_installer.git
cd openclaw_installer

# 查看当前状态
git status

# 添加修改的文件
git add .

# 提交更改
git commit -m "描述你的更改"

# 推送到远程仓库
git push
```

**分支管理**：
- `master` - 主分支，稳定版本
- 建议在开发新功能时创建新分支

### 工作空间配置

工作空间位于 `~/.openclaw/workspace/`，包含以下重要文件：

- **IDENTITY.md**：AI 助手的身份配置（名称、个性、头像等）
- **USER.md**：用户信息（姓名、称呼、时区等）
- **SOUL.md**：AI 助手的个性和行为准则
- **MEMORY.md**：长期记忆存储
- **TOOLS.md**：本地工具配置
- **HEARTBEAT.md**：心跳检查任务配置
- **AGENTS.md**：项目文档（本文件）
- **BOOTSTRAP.md**：初始化引导
- **SKILL.md**：技能说明

### 创建新技能

1. 在 `~/.openclaw/workspace/skills/` 下创建新目录
2. 创建 `SKILL.md` 文档
3. 创建 `scripts/` 目录和必要的脚本
4. 创建 `{skill_name}.skill` 标记文件

示例结构：
```
skills/
└── myskill/
    ├── SKILL.md
    ├── scripts/
    │   └── main.py
    └── myskill.skill
```

### 会话管理

会话历史存储在 `~/.openclaw/agents/main/sessions/`：
- `sessions.json`：会话索引
- `{uuid}.jsonl`：单个会话历史
- `.reset.*`：已重置的会话备份

### 定时任务

定时任务配置在 `~/.openclaw/cron/jobs.json`：

```json
{
  "version": 1,
  "jobs": []
}
```

### 托盘应用开发

托盘应用主程序位于 `tray_app.py`，基于以下技术：

- **pystray**：跨平台系统托盘库
- **Pillow**：图像处理库（用于创建图标）

**添加新功能**：
1. 编辑 `tray_app.py`
2. 在 `OpenClawTrayApp` 类中添加新方法
3. 在 `_create_menu()` 中添加菜单项
4. 运行 `start_tray.bat` 测试

**依赖安装**：
```bash
pip install pystray Pillow
```

**当前托盘应用特性**：
- 红色圆形图标（RGB: 220, 53, 69），白色 "OC" 文字
- 从 `~/.openclaw/openclaw.json` 动态读取配置
- 支持初始化设定功能（onboard 命令）
- 每 5 秒检查一次 Gateway 状态

## 配置说明

### Gateway 配置

- **端口**：18789（从配置文件读取）
- **模式**：local（本地模式）
- **绑定**：loopback（仅本地访问）
- **认证**：token 模式
- **禁止的命令**：
  - `camera.snap`
  - `camera.clip`
  - `screen.record`
  - `contacts.add`
  - `calendar.add`
  - `reminders.add`
  - `sms.send`

### AI 模型配置

- **提供商**：阿里云 DashScope
- **模型**：GLM-5
- **API 端点**：`https://coding.dashscope.aliyuncs.com/v1`
- **上下文窗口**：16,000 tokens
- **最大输出**：4,096 tokens

### 托盘应用配置

托盘应用配置在 `tray_app.py` 中：

- **配置文件路径**：`~/.openclaw/openclaw.json`（动态读取）
- **Web 界面 URL**：`http://localhost:{port}/#token={token}`（动态构建）
- **端口**：从配置文件读取（默认 18789）
- **图标**：红色圆形背景（RGB: 220, 53, 69），白色 "OC" 文字
- **状态检查**：每 5 秒检查一次 Gateway 状态

### 设备管理

设备身份信息存储在 `~/.openclaw/identity/device.json`：
- 设备 ID
- 公钥/私钥对（用于加密）
- 创建时间

配对的设备信息存储在 `~/.openclaw/devices/`：
- `paired.json`：已配对设备
- `pending.json`：待配对设备

## 故障排查

### 无法启动 Gateway

1. 检查端口 18789 是否被占用
2. 检查 Node.js 路径是否正确
3. 检查 `~/.openclaw/openclaw.json` 配置文件
4. 查看日志文件：`~/.openclaw/logs/`

### 托盘应用无法启动

1. 确保已安装 Python 3.12
2. 首次运行会自动安装依赖库（pystray、Pillow）
3. 手动安装依赖：
   ```bash
   pip install pystray Pillow
   ```
4. 检查 Windows 防火墙设置
5. 查看控制台输出的错误信息
6. 确认配置文件 `~/.openclaw/openclaw.json` 存在

### 托盘图标不显示

1. 检查 Pillow 是否正确安装
2. 尝试重新启动托盘应用
3. 检查 Windows 系统托盘设置（可能被隐藏）
4. 在任务管理器中查看是否有 `pythonw.exe` 进程正在运行
5. 检查 Windows 通知区域设置，确保托盘图标未设置为隐藏

### 配置未生效

1. 确认配置文件路径为 `~/.openclaw/openclaw.json`
2. 检查配置文件格式是否正确（JSON 格式）
3. 重启托盘应用以重新加载配置
4. 使用托盘应用的"查看状态"功能确认当前配置

### AI 模型无法响应

1. 检查 API key 是否有效
2. 检查网络连接
3. 检查 API 端点是否可访问
4. 查看 Gateway 日志

### 港股查询失败

1. 检查股票代码格式是否正确
2. 检查网络连接
3. 检查 Yahoo Finance API 是否可访问

### 股票新闻查询失败

1. 检查股票代码格式是否正确（美股、港股、A股）
2. 检查网络连接
3. 检查 Yahoo Finance API 是否可访问
4. 某些股票可能暂时没有相关新闻

### Shell 补全不工作

1. 确认补全脚本路径正确
2. 确认 Shell 类型匹配
3. 重新加载 Shell 配置
4. 检查脚本执行权限

### 开机自启动失败

1. 检查是否已安装到启动文件夹
2. 检查 `start_tray.bat` 路径是否正确
3. 检查 Windows 任务计划程序
4. 手动运行 `install_tray_startup.bat` 重新安装

## 最佳实践

### 1. 安全性

- 定期更新 API key
- 不要在公共网络暴露 Gateway
- 使用强密码保护 token
- 定期备份配置文件
- 不要分享您的 token 和 API key

### 2. 性能优化

- 定期清理会话历史
- 限制并发会话数量
- 使用适当的模型上下文窗口
- 缓存常用查询结果

### 3. 开发规范

- 保持配置文件格式一致
- 为新技能编写完整的文档
- 使用有意义的变量和函数名
- 添加错误处理和日志
- 遵循 Python PEP 8 代码风格

### 4. 备份策略

- 定期备份 `~/.openclaw/` 目录
- 保存重要的配置文件
- 记录关键配置更改
- 使用版本控制管理自定义代码

### 5. 托盘应用使用建议

- 推荐使用托盘应用作为主要启动方式（后台运行，不占用桌面空间）
- 设置开机自启动以保持服务可用
- 定期查看日志以监控服务状态
- 使用"查看状态"功能确认服务运行状态
- 托盘应用启动后，命令行窗口会自动关闭，这是正常行为
- 修改配置文件后，建议重启托盘应用以加载新配置

## 资源链接

### 代码仓库
- **GitHub 仓库**：https://github.com/wonglaitung/openclaw_installer

### 官方文档
- **OpenClaw 官方文档**：（待补充）

### AI 模型
- **阿里云 DashScope**：https://dashscope.aliyun.com/

### 数据源
- **Yahoo Finance API**：https://query2.finance.yahoo.com/

### 开发工具
- **Node.js 文档**：https://nodejs.org/docs/
- **Python 文档**：https://docs.python.org/3/
- **pystray 文档**：https://pystray.readthedocs.io/
- **Pillow 文档**：https://pillow.readthedocs.io/

## 版本信息

- **OpenClaw 版本**：2026.3.2
- **最后更新**：2026-03-11
- **最后配置**：2026-03-11
- **Git 仓库**：https://github.com/wonglaitung/openclaw_installer

## 更新日志

### 2026-03-11
- 更新托盘应用图标为红色圆形背景，白色 "OC" 文字
- 托盘应用改为从 `~/.openclaw/openclaw.json` 动态读取配置
- 添加"初始化设定"菜单项，支持执行 onboard 命令
- 新增 Yahoo Finance 股票新闻查询技能（yfinancenews）
- 更新文档，反映配置文件位置变更

### 2026-03-10
- 添加托盘应用功能
- 添加港股查询技能（aastocks）
- 更新 Git 工作流和版本控制文档

## 许可证

（待补充）

---

**维护者**：OpenClaw Team
**最后更新**：2026-03-11
**代码仓库**：https://github.com/wonglaitung/openclaw_installer