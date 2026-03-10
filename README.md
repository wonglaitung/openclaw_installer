# OpenClaw

OpenClaw 是一个基于 AI 的智能助手框架，提供命令行界面和 Web 界面两种交互方式，支持自定义 AI 模型、技能扩展和多种集成方式。

## 功能特性

- **多模态交互**：支持命令行和 Web 界面
- **系统托盘应用**：Windows 系统托盘集成，方便管理和控制
- **自定义 AI 模型**：集成阿里云 GLM-5 模型
- **技能系统**：支持扩展技能（如港股查询）
- **会话管理**：持久化会话历史和配置
- **设备管理**：支持设备配对和多设备访问
- **Shell 集成**：提供 Bash、Fish、PowerShell、Zsh 的自动补全支持

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

### 使用系统托盘应用

1. **启动托盘应用**：
   ```bash
   start_tray.bat
   ```

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

启动后，在 Windows 系统托盘区会显示蓝色图标（显示 "iF"）。右键点击图标可访问：

- **打开 Web 界面** - 直接在浏览器中打开 OpenClaw 界面
- **启动服务** - 手动启动 OpenClaw Gateway
- **停止服务** - 停止 OpenClaw Gateway
- **重启服务** - 重启 OpenClaw Gateway
- **查看状态** - 显示当前运行状态
- **打开日志目录** - 打开日志文件夹
- **打开配置文件** - 打开配置文件
- **退出** - 关闭托盘应用和 Gateway

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
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "your-token"
    }
  },
  "models": {
    "providers": {
      "custom-coding-dashscope-aliyuncs-com": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "your-api-key"
      }
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
│   ├── browser/                  # 浏览器相关配置
│   ├── completions/              # Shell 自动补全脚本
│   ├── cron/                     # 定时任务配置
│   ├── devices/                  # 设备配对信息
│   ├── identity/                 # 设备身份标识
│   ├── logs/                     # 日志文件
│   ├── workspace/                # 工作空间
│   │   ├── AGENTS.md             # 项目文档
│   │   ├── skills/               # 技能模块
│   │   │   └── aastocks/         # 港股查询技能
│   │   └── ...
│   └── openclaw.json             # 主配置文件
├── node-v22.21.1-win-x64/        # Node.js 运行环境
├── Python312/                    # Python 3.12 运行环境
├── start_openclaw.bat            # 主启动脚本
├── start_tray.bat                # 托盘应用启动脚本
├── install_tray_startup.bat      # 安装开机自启动
├── uninstall_tray_startup.bat    # 卸载开机自启动
└── tray_app.py                   # 托盘应用主程序
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
  - Python pystray
  - Pillow (图像处理)

## 常见问题

### 无法启动 Gateway

1. 检查端口 18789 是否被占用
2. 检查 Node.js 路径是否正确
3. 检查 `openclaw.json` 配置文件

### 托盘应用无法启动

1. 确保已安装 Python 3.12
2. 首次运行会自动安装依赖库（pystray、Pillow）
3. 检查 Windows 防火墙设置

### AI 模型无法响应

1. 检查 API key 是否有效
2. 检查网络连接
3. 检查 API 端点是否可访问

### 港股查询失败

1. 检查股票代码格式是否正确
2. 检查网络连接
3. 检查 Yahoo Finance API 是否可访问

## 安全建议

- 定期更新 API key
- 不要在公共网络暴露 Gateway
- 使用强密码保护 token
- 定期备份配置文件
- 不要分享您的 token 和 API key

## 开发

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

## 许可证

待补充

## 支持

如有问题或建议，请联系维护者或提交 Issue。

## 版本信息

- **OpenClaw 版本**：2026.3.2
- **最后更新**：2026-03-09