import sys
import os
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import websockets
from realtime_dialog_client import RealtimeDialogClient
import config
import pytest

class TestRealtimeDialogClient:
    """测试realtime_dialog_client.py模块"""

    def setup_method(self):
        """设置测试环境"""
        # 创建一个模拟的WebSocket配置
        self.ws_config = {
            "base_url": "wss://test.example.com",
            "headers": {
                "X-Api-App-ID": "test-app-id",
                "X-Api-Access-Key": "test-access-key",
                "X-Api-Resource-Id": "test-resource-id",
                "X-Api-App-Key": "test-app-key",
                "X-Api-Connect-Id": "test-connect-id"
            }
        }
        self.session_id = "test_session_id"
        
    @patch('realtime_dialog_client.websockets')
    @pytest.mark.asyncio
    async def test_init(self, mock_websockets):
        """测试RealtimeDialogClient初始化"""
        client = RealtimeDialogClient(self.ws_config, self.session_id)
        assert client.config == self.ws_config
        assert client.session_id == self.session_id
        assert client.ws is None
        assert client.logid == ""
        
    @patch('realtime_dialog_client.websockets')
    @pytest.mark.asyncio
    async def test_connect(self, mock_websockets):
        """测试连接方法"""
        # 创建模拟WebSocket对象
        mock_ws = AsyncMock()  # 使用AsyncMock
        mock_ws.response_headers = {"X-Tt-Logid": "test_logid"}
        # 设置websockets.connect返回一个协程，该协程返回mock_ws
        mock_websockets.connect = AsyncMock(return_value=mock_ws)
        
        # 创建客户端实例
        client = RealtimeDialogClient(self.ws_config, self.session_id)
        
        # 调用connect方法
        await client.connect()
        
        # 验证连接被调用
        mock_websockets.connect.assert_called_with(
            self.ws_config['base_url'],
            extra_headers=self.ws_config['headers'],
            ping_interval=None
        )
        
        # 验证日志ID被设置
        assert client.logid == "test_logid"
        
        # 验证发送了StartConnection和StartSession请求
        assert mock_ws.send.call_count == 2
        
    @patch('realtime_dialog_client.websockets')
    @pytest.mark.asyncio
    async def test_say_hello(self, mock_websockets):
        """测试say_hello方法"""
        # 创建模拟WebSocket对象
        mock_ws = AsyncMock()  # 使用AsyncMock
        # 设置websockets.connect返回一个协程，该协程返回mock_ws
        mock_websockets.connect = AsyncMock(return_value=mock_ws)
        
        # 创建客户端实例并连接
        client = RealtimeDialogClient(self.ws_config, self.session_id)
        client.ws = mock_ws
        
        # 调用say_hello方法
        await client.say_hello()
        
        # 验证发送了hello请求
        mock_ws.send.assert_called_once()
        
    @patch('realtime_dialog_client.websockets')
    @pytest.mark.asyncio
    async def test_chat_tts_text(self, mock_websockets):
        """测试chat_tts_text方法"""
        # 创建模拟WebSocket对象
        mock_ws = AsyncMock()  # 使用AsyncMock
        # 设置websockets.connect返回一个协程，该协程返回mock_ws
        mock_websockets.connect = AsyncMock(return_value=mock_ws)
        
        # 创建客户端实例并连接
        client = RealtimeDialogClient(self.ws_config, self.session_id)
        client.ws = mock_ws
        
        # 调用chat_tts_text方法 (is_user_querying=False)
        await client.chat_tts_text(False, True, False, "test content")
        
        # 验证发送了chat_tts_text请求
        mock_ws.send.assert_called_once()
        
        # 重置mock并测试is_user_querying=True的情况
        mock_ws.send.reset_mock()
        await client.chat_tts_text(True, True, False, "test content")
        # 当is_user_querying为True时，不应发送请求
        mock_ws.send.assert_not_called()
        
    @patch('realtime_dialog_client.websockets')
    @pytest.mark.asyncio
    async def test_task_request(self, mock_websockets):
        """测试task_request方法"""
        # 创建模拟WebSocket对象
        mock_ws = AsyncMock()  # 使用AsyncMock
        # 设置websockets.connect返回一个协程，该协程返回mock_ws
        mock_websockets.connect = AsyncMock(return_value=mock_ws)
        
        # 创建客户端实例并连接
        client = RealtimeDialogClient(self.ws_config, self.session_id)
        client.ws = mock_ws
        
        # 调用task_request方法
        test_audio = b"test_audio_data"
        await client.task_request(test_audio)
        
        # 验证发送了task请求
        mock_ws.send.assert_called_once()
        
    @patch('realtime_dialog_client.websockets')
    @pytest.mark.asyncio
    async def test_receive_server_response(self, mock_websockets):
        """测试receive_server_response方法"""
        # 创建模拟WebSocket对象
        mock_ws = AsyncMock()  # 使用AsyncMock
        # 设置websockets.connect返回一个协程，该协程返回mock_ws
        mock_websockets.connect = AsyncMock(return_value=mock_ws)
        
        # 创建客户端实例并连接
        client = RealtimeDialogClient(self.ws_config, self.session_id)
        client.ws = mock_ws
        
        # 模拟接收响应
        mock_response = b"test_response_data"
        mock_ws.recv = AsyncMock(return_value=mock_response)
        
        # 调用receive_server_response方法
        with patch('realtime_dialog_client.protocol.parse_response') as mock_parse:
            mock_parse.return_value = {"test": "data"}
            result = await client.receive_server_response()
            
            # 验证结果
            assert result == {"test": "data"}
            mock_ws.recv.assert_called_once()
            mock_parse.assert_called_with(mock_response)
            
    @patch('realtime_dialog_client.websockets')
    @pytest.mark.asyncio
    async def test_finish_session(self, mock_websockets):
        """测试finish_session方法"""
        # 创建模拟WebSocket对象
        mock_ws = AsyncMock()  # 使用AsyncMock
        # 设置websockets.connect返回一个协程，该协程返回mock_ws
        mock_websockets.connect = AsyncMock(return_value=mock_ws)
        
        # 创建客户端实例并连接
        client = RealtimeDialogClient(self.ws_config, self.session_id)
        client.ws = mock_ws
        
        # 调用finish_session方法
        await client.finish_session()
        
        # 验证发送了finish_session请求
        mock_ws.send.assert_called_once()
        
    @patch('realtime_dialog_client.websockets')
    @pytest.mark.asyncio
    async def test_finish_connection(self, mock_websockets):
        """测试finish_connection方法"""
        # 创建模拟WebSocket对象
        mock_ws = AsyncMock()  # 使用AsyncMock
        # 设置websockets.connect返回一个协程，该协程返回mock_ws
        mock_websockets.connect = AsyncMock(return_value=mock_ws)
        
        # 创建客户端实例并连接
        client = RealtimeDialogClient(self.ws_config, self.session_id)
        client.ws = mock_ws
        
        # 调用finish_connection方法
        await client.finish_connection()
        
        # 验证发送了finish_connection请求
        mock_ws.send.assert_called_once()
        
    @patch('realtime_dialog_client.websockets')
    @pytest.mark.asyncio
    async def test_close(self, mock_websockets):
        """测试close方法"""
        # 创建模拟WebSocket对象
        mock_ws = AsyncMock()  # 使用AsyncMock
        # 设置websockets.connect返回一个协程，该协程返回mock_ws
        mock_websockets.connect = AsyncMock(return_value=mock_ws)
        
        # 创建客户端实例并连接
        client = RealtimeDialogClient(self.ws_config, self.session_id)
        client.ws = mock_ws
        
        # 调用close方法
        await client.close()
        
        # 验证WebSocket连接被关闭
        mock_ws.close.assert_called_once()