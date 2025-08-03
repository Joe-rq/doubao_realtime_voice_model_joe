import sys
import os
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 测试主模块
import main

class TestMain(unittest.TestCase):
    """测试main.py模块"""

    @patch('main.DialogSession')
    def test_main_function(self, mock_dialog_session):
        """测试main函数"""
        # 创建模拟对象
        mock_session_instance = MagicMock()
        # 设置模拟对象的start方法为异步方法
        mock_session_instance.start = AsyncMock()
        mock_dialog_session.return_value = mock_session_instance
        
        # 创建一个异步函数来运行main
        async def run_main():
            await main.main()
        
        # 运行异步函数
        asyncio.run(run_main())
        
        # 验证DialogSession被正确创建
        mock_dialog_session.assert_called_with(main.config.ws_connect_config)
        # 验证start方法被调用
        mock_session_instance.start.assert_called_once()

if __name__ == '__main__':
    unittest.main()