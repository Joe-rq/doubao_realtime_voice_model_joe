#!/usr/bin/env python3
"""
安装测试脚本 - 验证环境和依赖
"""

import sys
import subprocess

def test_import(module_name, description):
    """测试模块导入"""
    try:
        __import__(module_name)
        print(f"✓ {description}")
        return True
    except ImportError as e:
        print(f"✗ {description}: {e}")
        return False

def main():
    """运行安装测试"""
    print("🔍 环境测试 - 英文视频同声传译工具")
    print("=" * 40)
    
    # Python 版本检查
    print(f"Python 版本: {sys.version}")
    
    # 测试核心依赖
    dependencies = [
        ("pyaudio", "音频处理库 PyAudio"),
        ("websockets", "WebSocket 客户端"),
        ("numpy", "数值计算库 NumPy"),
        ("json", "JSON 处理"),
        ("asyncio", "异步IO支持")
    ]
    
    failed = []
    for module, desc in dependencies:
        if not test_import(module, desc):
            failed.append(module)
    
    print("\n" + "=" * 40)
    
    if failed:
        print(f"❌ 发现 {len(failed)} 个缺失的依赖:")
        for module in failed:
            print(f"   - {module}")
        print("\n请运行以下命令安装:")
        print("  python setup.py")
        print("或")
        print("  pip install -r requirements.txt")
    else:
        print("🎉 所有依赖已就绪！")
        print("\n下一步:")
        print("1. 编辑 config.py 设置API凭证")
        print("2. 运行: python translator.py")

if __name__ == "__main__":
    main()