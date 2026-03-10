# OpenClaw

OpenClaw 是一个基于 AI 的智能助手框架，提供命令行界面、Web 界面和系统托盘应用三种交互方式，支持自定义 AI 模型、技能扩展和多种集成方式，特别适合 Windows 用户进行本地化 AI 助手部署。

## 项目信息

- **GitHub 仓库**：https://github.com/wonglaitung/openclaw_installer
- **版本**：2026.3.2
- **最后更新**：2026-03-10

## 功能特性

- **多模态交互**：支持命令行、Web 界面和系统托盘应用
- **系统托盘集成**：Windows 原生托盘应用，支持开机自启动和图形化管理，后台运行无干扰
- **自定义 AI 模型**：集成阿里云 GLM-5 模型（通过自定义提供商）
- **技能系统**：支持扩展技能（如港股查询）
- **会话管理**：持久化会话历史和配置
- **设备管理**：支持设备配对和多设备访问
- **Shell 集成**：提供多种 Shell 的自动补全支持
- **便捷管理**：一键启动/停止/重启服务，快速访问日志和配置
- **代码管理**：支持 Git 版本控制，代码托管在 GitHub

## 快速开始

### 系统要求

- Windows 10/11 或 WSL2
- Node.js v22.21.1（已包含）
- Python 3.12（已包含）

### 安装步骤

1. **首次初始化**：
   ```bash
   start_openclaw.bat onboard
   ```

2. **启动 Gateway**：
   ```bash
   start_openclaw.bat
   ```

3. **访问 Web 界面**：
   - 启动后会自动打开浏览器
   - 访问：`http://localhost:18789`

### 使用系统托盘应用（推荐）

1. **启动托盘应用**：
   ```bash
   start_tray.bat
   ```

   **启动特性**：
   - 双击 `start_tray.bat` 后，命令行窗口会快速关闭
   - 托盘应用在后台运行，不会显示命令行窗口
   - OpenClaw 图标会自动出现在 Windows 系统托盘区（蓝色圆形图标，显示 "iF"）
   - Gateway 服务会自动启动

2. **设置开机自启动**：
   ```bash
   install_tray_startup.bat
   ```

3. **卸载开机自启动**：
   ```bash
   uninstall_tray_startup.bat
   ```

## 使用指南

### 命令行模式

```bash
# 默认模式（Gateway + Web）
start_openclaw.bat

# 仅启动 Gateway（不打开网页）
start_openclaw.bat onboard

# Gateway 模式（打开网页）
start_openclaw.bat gateway
```

### 系统托盘应用

启动后，在 Windows 系统托盘区会显示蓝色图标（显示 "iF"）。右键点击图标可访问以下功能：

- **打开 Web 界面** - 直接在浏览器中打开 OpenClaw 界面
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

### 港股查询技能

```bash
cd .openclaw/workspace/skills/aastocks/scripts
python3 fetch_stock.py 01398  # 工商银行
python3 fetch_stock.py 0700   # 腾讯控股
python3 fetch_stock.py 0001   # 长和
```

### Shell 自动补全

**Bash**：
```bash
source .openclaw/completions/openclaw.bash
```

**Zsh**：
```bash
source .openclaw/completions/openclaw.zsh
```

**PowerShell**：
```powershell
. ".openclaw/completions/openclaw.ps1"
```

## 配置说明

### 主配置文件

配置文件位于 `.openclaw/openclaw.json`：

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

### 工作空间配置

工作空间位于 `.openclaw/workspace/`：

- **IDENTITY.md** - AI 助手的身份配置
- **USER.md** - 用户信息
- **SOUL.md** - AI 助手的个性和行为准则
- **MEMORY.md** - 长期记忆存储
- **TOOLS.md** - 本地工具配置

## 项目结构

```
openclaw/
├── .openclaw/                    # 主配置目录
│   ├── agents/                   # 代理配置
│   │   └── main/                 # 主代理
│   │       ├── agent/            # 代理配置文件
│   │       └── sessions/         # 会话历史
│   ├── browser/                  # 浏览器相关配置
│   ├── canvas/                   # 画布功能
│   ├── completions/              # Shell 自动补全脚本
│   │   ├── openclaw.bash
│   │   ├── openclaw.fish
│   │   ├── openclaw.ps1
│   │   └── openclaw.zsh
│   ├── cron/                     # 定时任务配置
│   │   └── jobs.json
│   ├── devices/                  # 设备配对信息
│   │   ├── paired.json
│   │   └── pending.json
│   ├── identity/                 # 设备身份标识
│   │   └── device.json
│   ├── logs/                     # 日志文件
│   ├── workspace/                # 工作空间
│   │   ├── AGENTS.md             # 项目文档
│   │   ├── BOOTSTRAP.md          # 初始化引导
│   │   ├── HEARTBEAT.md          # 心跳检查配置
│   │   ├── IDENTITY.md           # AI 身份配置
│   │   ├── MEMORY.md             # 长期记忆
│   │   ├── SKILL.md              # 技能说明
│   │   ├── SOUL.md               # AI 个性配置
│   │   ├── TOOLS.md              # 工具配置
│   │   ├── USER.md               # 用户信息
│   │   ├── .git/                 # Git 仓库
│   │   ├── .openclaw/            # 工作空间配置
│   │   └── skills/               # 技能模块
│   │       └── aastocks/         # 港股查询技能
│   │           ├── SKILL.md      # 技能文档
│   │           └── scripts/      # 脚本
│   │               └── fetch_stock.py
│   ├── gateway.cmd               # Gateway 启动脚本
│   ├── openclaw.json             # 主配置文件
│   └── update-check.json         # 更新检查配置
├── node-v22.21.1-win-x64/        # Node.js 运行环境
│   ├── node.exe
│   ├── npm
│   ├── npx
│   └── node_modules/
│   └── openclaw/                 # OpenClaw 核心包
├── Python312/                    # Python 3.12 运行环境
│   ├── python.exe
│   └── Lib/                      # Python 标准库
├── start_openclaw.bat            # 主启动脚本
├── start_tray.bat                # 托盘应用启动脚本
├── install_tray_startup.bat      # 安装开机自启动
├── uninstall_tray_startup.bat    # 卸载开机自启动
├── tray_app.py                   # 托盘应用主程序
├── README.md                     # 项目说明文档
├── AGENTS.md                     # 项目文档
└── .git/                         # Git 版本控制
```

## 技术栈

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

## 常见问题

### 无法启动 Gateway

1. 检查端口 18789 是否被占用
2. 检查 Node.js 路径是否正确
3. 检查 `openclaw.json` 配置文件
4. 查看日志文件：`.openclaw/logs/`

### 托盘应用无法启动

1. 确保已安装 Python 3.12
2. 首次运行会自动安装依赖库（pystray、Pillow）
3. 手动安装依赖：
   ```bash
   pip install pystray Pillow
   ```
4. 检查 Windows 防火墙设置
5. 查看控制台输出的错误信息

### 托盘图标不显示

1. 检查 Pillow 是否正确安装
2. 尝试重新启动托盘应用
3. 检查 Windows 系统托盘设置（可能被隐藏）
4. 在任务管理器中查看是否有 `pythonw.exe` 进程正在运行
5. 检查 Windows 通知区域设置，确保托盘图标未设置为隐藏

### AI 模型无法响应

1. 检查 API key 是否有效
2. 检查网络连接
3. 检查 API 端点是否可访问
4. 查看 Gateway 日志

### 港股查询失败

1. 检查股票代码格式是否正确
2. 检查网络连接
3. 检查 Yahoo Finance API 是否可访问

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

## 安全建议

- 定期更新 API key
- 不要在公共网络暴露 Gateway
- 使用强密码保护 token
- 定期备份配置文件
- 不要分享您的 token 和 API key
- 定期备份 `.openclaw/` 目录
- 使用版本控制管理自定义代码

## 开发

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

### 创建新技能

1. 在 `.openclaw/workspace/skills/` 下创建新目录
2. 创建 `SKILL.md` 文档
3. 创建 `scripts/` 目录和必要的脚本
4. 创建 `{skill_name}.skill` 二进制文件

### 贡献指南

欢迎贡献代码和建议。请遵循以下规范：

- 保持配置文件格式一致
- 为新技能编写完整的文档
- 使用有意义的变量和函数名
- 添加错误处理和日志
- 遵循 Python PEP 8 代码风格

## 许可证

（待补充）

---

**维护者**：OpenClaw Team
**最后更新**：2026-03-10
**代码仓库**：https://github.com/wonglaitung/openclaw_installer

## 支持

如有问题或建议，请联系维护者或提交 Issue：

- **GitHub Issues**：https://github.com/wonglaitung/openclaw_installer/issues
- **代码仓库**：https://github.com/wonglaitung/openclaw_installer

## 资源链接

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
- **最后更新**：2026-03-10
- **最后配置**：2026-03-10
- **Git 仓库**：https://github.com/wonglaitung/openclaw_installer