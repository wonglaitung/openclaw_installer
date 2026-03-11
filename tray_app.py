#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 系统托盘应用
提供 Windows 系统托盘图标，用于管理和控制 OpenClaw Gateway 服务
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

# 尝试导入 pystray 和 Pillow
try:
    import pystray
    # Pillow 的导入
    import PIL
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print("错误：需要安装 pystray 和 Pillow")
    print(f"详细错误：{e}")
    print("请运行：pip install pystray Pillow")
    sys.exit(1)


class OpenClawTrayApp:
    """OpenClaw 系统托盘应用类"""

    def __init__(self):
        # 获取脚本所在目录
        self.base_path = Path(__file__).parent.resolve()
        self.node_path = self.base_path / "node-v22.21.1-win-x64"
        self.python_path = self.base_path / "Python312"

        # 读取配置文件
        self._load_config()

    def _load_config(self):
        """从配置文件加载配置"""
        # 配置文件位于用户主目录下的 .openclaw 文件夹
        config_path = Path.home() / ".openclaw" / "openclaw.json"

        # 默认值
        self.port = 18789
        self.token = ""
        self.web_url = f"http://localhost:{self.port}/"

        # 尝试读取配置文件
        if config_path.exists():
            try:
                import json
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # 读取端口
                if 'gateway' in config and 'port' in config['gateway']:
                    self.port = config['gateway']['port']

                # 读取 token
                if 'gateway' in config and 'auth' in config['gateway'] and 'token' in config['gateway']['auth']:
                    self.token = config['gateway']['auth']['token']

                # 构建 Web URL
                if self.token:
                    self.web_url = f"http://localhost:{self.port}/#token={self.token}"
                else:
                    self.web_url = f"http://localhost:{self.port}/"

                print(f"配置加载成功: 端口={self.port}, token={'已设置' if self.token else '未设置'}")
            except Exception as e:
                print(f"读取配置文件失败：{e}，使用默认配置")
        else:
            print(f"配置文件不存在：{config_path}，使用默认配置")
        
        # 进程管理
        self.gateway_process = None
        self.is_running = False
        self.status_message = "OpenClaw - 已停止"
        
        # 创建托盘图标
        self.icon = None
        self._create_icon()
        
    def _create_icon(self):
        """创建托盘图标"""
        # 创建一个简单的图标（红色圆形背景，白色 "OC" 文字）
        try:
            # 创建 RGBA 图像
            image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)

            # 绘制圆形背景（红色）
            draw.ellipse([4, 4, 60, 60], fill=(220, 53, 69, 255))

            # 绘制文字 "OC"
            try:
                # 尝试使用 Arial 字体
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                # 如果找不到 Arial，使用默认字体
                font = ImageFont.load_default()

            # 绘制文字
            draw.text((14, 12), "OC", fill=(255, 255, 255, 255), font=font)
            
            self.icon_image = image
            print("图标创建成功")
        except Exception as e:
            print(f"创建图标失败：{e}")
            # 创建一个简单的备用图标（纯色方块）
            try:
                image = Image.new('RGB', (64, 64), (220, 53, 69))
                self.icon_image = image
                print("使用备用图标")
            except Exception as e2:
                print(f"创建备用图标也失败：{e2}")
                self.icon_image = None
    
    def _setup_environment(self):
        """设置环境变量"""
        # 添加 Node.js 和 Python 到 PATH
        env = os.environ.copy()
        
        node_path_str = str(self.node_path)
        python_path_str = str(self.python_path)
        
        if node_path_str not in env.get('PATH', ''):
            env['PATH'] = node_path_str + os.pathsep + env.get('PATH', '')
        
        if python_path_str not in env.get('PATH', ''):
            env['PATH'] = python_path_str + os.pathsep + env.get('PATH', '')
        
        return env
    
    def _start_gateway(self):
        """启动 OpenClaw Gateway"""
        if self.gateway_process and self.gateway_process.poll() is None:
            print("Gateway 已经在运行中")
            return True
        
        try:
            env = self._setup_environment()
            
            # 构建命令
            openclaw_cmd = str(self.node_path / "node.exe")
            openclaw_script = str(self.node_path / "node_modules" / "openclaw" / "dist" / "index.js")
            
            print(f"启动 Gateway: {openclaw_cmd} {openclaw_script} gateway")
            
            # 启动进程
            self.gateway_process = subprocess.Popen(
                [openclaw_cmd, openclaw_script, "gateway", "--port", str(self.port)],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # 等待启动
            time.sleep(2)
            
            if self.gateway_process.poll() is None:
                self.is_running = True
                self.status_message = "OpenClaw - 运行中"
                print("Gateway 启动成功")
                return True
            else:
                print("Gateway 启动失败")
                return False
                
        except Exception as e:
            print(f"启动 Gateway 时出错：{e}")
            return False
    
    def _stop_gateway(self):
        """停止 OpenClaw Gateway"""
        if self.gateway_process and self.gateway_process.poll() is None:
            try:
                self.gateway_process.terminate()
                # 等待进程结束
                self.gateway_process.wait(timeout=5)
                print("Gateway 已停止")
            except subprocess.TimeoutExpired:
                # 如果进程没有响应，强制终止
                self.gateway_process.kill()
                print("Gateway 已强制停止")
            except Exception as e:
                print(f"停止 Gateway 时出错：{e}")
        
        self.gateway_process = None
        self.is_running = False
        self.status_message = "OpenClaw - 已停止"
    
    def _restart_gateway(self):
        """重启 OpenClaw Gateway"""
        print("重启 Gateway...")
        self._stop_gateway()
        time.sleep(1)
        self._start_gateway()
    
    def _check_gateway_status(self):
        """检查 Gateway 状态"""
        if self.gateway_process and self.gateway_process.poll() is None:
            return True
        return False
    
    # 菜单回调函数
    def on_open_web(self, icon, item):
        """打开 Web 界面"""
        print("打开 Web 界面...")
        webbrowser.open(self.web_url)

    def on_onboard(self, icon, item):
        """执行 OpenClaw 初始化设定"""
        print("执行 OpenClaw 初始化设定...")
        try:
            env = self._setup_environment()

            # 构建命令
            openclaw_cmd = str(self.node_path / "node.exe")
            openclaw_script = str(self.node_path / "node_modules" / "openclaw" / "dist" / "index.js")

            print(f"运行: {openclaw_cmd} {openclaw_script} onboard")

            # 使用 subprocess 启动命令，在新窗口中显示
            subprocess.Popen(
                [openclaw_cmd, openclaw_script, "onboard"],
                env=env,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            print("onboard 命令已启动")
        except Exception as e:
            print(f"执行 onboard 命令时出错：{e}")
            self.icon.notify(f"执行失败：{e}", "OpenClaw Onboard")
    
    def on_start(self, icon, item):
        """启动服务"""
        print("启动服务...")
        if not self._check_gateway_status():
            self._start_gateway()
        else:
            print("服务已经在运行中")
    
    def on_stop(self, icon, item):
        """停止服务"""
        print("停止服务...")
        self._stop_gateway()
    
    def on_restart(self, icon, item):
        """重启服务"""
        print("重启服务...")
        self._restart_gateway()
    
    def on_status(self, icon, item):
        """显示状态"""
        status = "运行中" if self._check_gateway_status() else "已停止"
        print(f"当前状态：{status}")
        # 显示通知
        self.icon.notify(f"当前状态：{status}", "OpenClaw 状态")
    
    def on_show_logs(self, icon, item):
        """显示日志目录"""
        log_path = self.base_path / ".openclaw" / "logs"
        if log_path.exists():
            print(f"打开日志目录：{log_path}")
            os.startfile(str(log_path))
        else:
            print("日志目录不存在")
    
    def on_open_config(self, icon, item):
        """打开配置文件"""
        config_path = self.base_path / ".openclaw" / "openclaw.json"
        if config_path.exists():
            print(f"打开配置文件：{config_path}")
            os.startfile(str(config_path))
        else:
            print("配置文件不存在")
    
    def on_quit(self, icon, item):
        """退出应用"""
        print("退出应用...")
        self._stop_gateway()
        icon.stop()
    
    def _create_menu(self):
        """创建右键菜单"""
        menu_items = [
            pystray.MenuItem('打开 Web 界面', self.on_open_web),
            pystray.MenuItem('初始化设定', self.on_onboard),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('启动服务', self.on_start),
            pystray.MenuItem('停止服务', self.on_stop),
            pystray.MenuItem('重启服务', self.on_restart),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('查看状态', self.on_status),
            pystray.MenuItem('打开日志目录', self.on_show_logs),
            pystray.MenuItem('打开配置文件', self.on_open_config),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('退出', self.on_quit),
        ]
        return pystray.Menu(*menu_items)
    
    def _status_check_thread(self):
        """状态检查线程"""
        while self.is_running:
            time.sleep(5)
            # 检查进程状态
            if self.gateway_process and self.gateway_process.poll() is not None:
                print("Gateway 进程意外退出")
                self.is_running = False
                self.status_message = "OpenClaw - 已停止"
    
    def run(self):
        """运行托盘应用"""
        print("启动 OpenClaw 系统托盘应用...")
        
        # 自动启动 Gateway
        if self._start_gateway():
            print("Gateway 启动成功")
        else:
            print("Gateway 启动失败")
        
        # 创建托盘图标
        try:
            if self.icon_image:
                self.icon = pystray.Icon(
                    "OpenClaw",
                    self.icon_image,
                    "OpenClaw",
                    self._create_menu()
                )
            else:
                # 使用默认图标（字符串）
                self.icon = pystray.Icon(
                    "OpenClaw",
                    "OpenClaw",
                    "OpenClaw",
                    self._create_menu()
                )
            
            # 显示启动通知
            try:
                self.icon.notify("OpenClaw Gateway 已启动", "启动成功")
                print("启动通知已显示")
            except Exception as e:
                print(f"显示通知失败：{e}")
        except Exception as e:
            print(f"创建托盘图标失败：{e}")
            return False
        
        # 启动状态检查线程
        status_thread = threading.Thread(target=self._status_check_thread, daemon=True)
        status_thread.start()
        
        # 运行托盘应用
        print("托盘应用已启动，右键点击图标查看菜单")
        try:
            self.icon.run()
        except KeyboardInterrupt:
            print("\n用户中断")
        except Exception as e:
            print(f"托盘应用运行出错：{e}")
        
        print("托盘应用已退出")
        return True


def main():
    """主函数"""
    try:
        app = OpenClawTrayApp()
        app.run()
    except KeyboardInterrupt:
        print("\n应用被用户中断")
    except Exception as e:
        print(f"应用运行出错：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()