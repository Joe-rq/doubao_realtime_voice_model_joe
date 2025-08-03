#!/usr/bin/env python3
"""
安装脚本 - 简化依赖安装和环境配置
"""

import subprocess
import sys
import os

def run_command(command, description=""):
    """运行命令并处理错误"""
    print(f"{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} 失败: {e.stderr}")
        return False

def check_uv():
    """检查是否安装了 uv"""
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    """主安装流程"""
    print("🚀 英文视频同声传译工具 - 安装脚本")
    print("=" * 50)
    
    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print("❌ 需要 Python 3.8 或更高版本")
        return False
    
    print(f"✓ Python {sys.version.split()[0]} 检测成功")
    
    # 检查 uv 是否可用
    use_uv = check_uv()
    if use_uv:
        print("✓ 检测到 uv，将使用 uv 进行依赖管理")
    else:
        print("⚠ 未检测到 uv，将使用 pip 进行安装")
        print("  建议安装 uv: pip install uv")
    
    # 安装依赖
    if use_uv:
        success = run_command("uv pip install -r requirements.txt", "使用 uv 安装依赖")
    else:
        success = run_command(f"{sys.executable} -m pip install -r requirements.txt", "使用 pip 安装依赖")
    
    if not success:
        print("\n❌ 依赖安装失败，请手动运行:")
        if use_uv:
            print("  uv pip install -r requirements.txt")
        else:
            print("  pip install -r requirements.txt")
        return False
    
    print("\n🎉 安装完成！")
    print("\n下一步:")
    print("1. 编辑 config.py 设置你的豆包API凭证")
    print("2. 运行: python translator.py")
    print("3. 或双击 run.bat 启动")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)