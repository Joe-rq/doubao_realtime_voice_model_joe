import sys
import os
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import queue

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audio_manager import AudioConfig, AudioDeviceManager, DialogSession
from realtime_dialog_client import RealtimeDialogClient
import config

class TestAudioManager(unittest.TestCase):
    """测试audio_manager.py模块"""

    def test_audio_config_creation(self):
        """测试AudioConfig数据类的创建"""
        audio_config = AudioConfig(
            format="pcm",
            bit_size=16,
            channels=1,
            sample_rate=16000,
            chunk=1024
        )
        self.assertEqual(audio_config.format, "pcm")
        self.assertEqual(audio_config.bit_size, 16)
        self.assertEqual(audio_config.channels, 1)
        self.assertEqual(audio_config.sample_rate, 16000)
        self.assertEqual(audio_config.chunk, 1024)
        
    @patch('audio_manager.pyaudio.PyAudio')
    def test_audio_device_manager_init(self, mock_pyaudio):
        """测试AudioDeviceManager初始化"""
        input_config = AudioConfig(**config.input_audio_config)
        output_config = AudioConfig(**config.output_audio_config)
        
        manager = AudioDeviceManager(input_config, output_config)
        self.assertEqual(manager.input_config, input_config)
        self.assertEqual(manager.output_config, output_config)
        self.assertIsNone(manager.input_stream)
        self.assertIsNone(manager.output_stream)
        mock_pyaudio.assert_called_once()
        
    @patch('audio_manager.pyaudio.PyAudio')
    def test_open_input_stream(self, mock_pyaudio):
        """测试打开音频输入流"""
        mock_stream = MagicMock()
        mock_pyaudio_instance = MagicMock()
        mock_pyaudio.return_value = mock_pyaudio_instance
        mock_pyaudio_instance.open.return_value = mock_stream
        
        input_config = AudioConfig(**config.input_audio_config)
        output_config = AudioConfig(**config.output_audio_config)
        manager = AudioDeviceManager(input_config, output_config)
        
        stream = manager.open_input_stream()
        self.assertEqual(stream, mock_stream)
        mock_pyaudio_instance.open.assert_called_with(
            format=input_config.bit_size,
            channels=input_config.channels,
            rate=input_config.sample_rate,
            input=True,
            frames_per_buffer=input_config.chunk
        )
        
    @patch('audio_manager.pyaudio.PyAudio')
    def test_open_output_stream(self, mock_pyaudio):
        """测试打开音频输出流"""
        mock_stream = MagicMock()
        mock_pyaudio_instance = MagicMock()
        mock_pyaudio.return_value = mock_pyaudio_instance
        mock_pyaudio_instance.open.return_value = mock_stream
        
        input_config = AudioConfig(**config.input_audio_config)
        output_config = AudioConfig(**config.output_audio_config)
        manager = AudioDeviceManager(input_config, output_config)
        
        stream = manager.open_output_stream()
        self.assertEqual(stream, mock_stream)
        mock_pyaudio_instance.open.assert_called_with(
            format=output_config.bit_size,
            channels=output_config.channels,
            rate=output_config.sample_rate,
            output=True,
            frames_per_buffer=output_config.chunk
        )
        
    @patch('audio_manager.pyaudio.PyAudio')
    def test_cleanup(self, mock_pyaudio):
        """测试清理音频设备资源"""
        mock_input_stream = MagicMock()
        mock_output_stream = MagicMock()
        mock_pyaudio_instance = MagicMock()
        mock_pyaudio.return_value = mock_pyaudio_instance
        
        input_config = AudioConfig(**config.input_audio_config)
        output_config = AudioConfig(**config.output_audio_config)
        manager = AudioDeviceManager(input_config, output_config)
        manager.input_stream = mock_input_stream
        manager.output_stream = mock_output_stream
        
        manager.cleanup()
        
        mock_input_stream.stop_stream.assert_called_once()
        mock_input_stream.close.assert_called_once()
        mock_output_stream.stop_stream.assert_called_once()
        mock_output_stream.close.assert_called_once()
        mock_pyaudio_instance.terminate.assert_called_once()

class TestDialogSession(unittest.TestCase):
    """测试DialogSession类"""
    
    def setUp(self):
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
        
    @patch('audio_manager.RealtimeDialogClient')
    @patch('audio_manager.AudioDeviceManager')
    def test_dialog_session_init(self, mock_audio_device_manager, mock_realtime_client):
        """测试DialogSession初始化"""
        # 创建模拟对象
        mock_audio_device_instance = MagicMock()
        mock_audio_device_manager.return_value = mock_audio_device_instance
        mock_client_instance = MagicMock()
        mock_realtime_client.return_value = mock_client_instance
        
        # 创建DialogSession实例
        session = DialogSession(self.ws_config)
        
        # 验证初始化
        self.assertTrue(hasattr(session, 'session_id'))
        self.assertEqual(session.client, mock_client_instance)
        self.assertEqual(session.audio_device, mock_audio_device_instance)
        self.assertTrue(session.is_running)
        self.assertFalse(session.is_session_finished)
        self.assertFalse(session.is_user_querying)
        self.assertFalse(session.is_sending_chat_tts_text)
        self.assertEqual(session.audio_buffer, b'')
        
    @patch('audio_manager.RealtimeDialogClient')
    @patch('audio_manager.AudioDeviceManager')
    def test_handle_server_response_empty(self, mock_audio_device_manager, mock_realtime_client):
        """测试处理空服务器响应"""
        # 创建模拟对象
        mock_audio_device_instance = MagicMock()
        mock_audio_device_manager.return_value = mock_audio_device_instance
        mock_client_instance = MagicMock()
        mock_realtime_client.return_value = mock_client_instance
        
        # 创建DialogSession实例
        session = DialogSession(self.ws_config)
        
        # 测试空响应
        session.handle_server_response({})
        # 没有异常即为通过
        
    @patch('audio_manager.RealtimeDialogClient')
    @patch('audio_manager.AudioDeviceManager')
    def test_handle_server_response_ack(self, mock_audio_device_manager, mock_realtime_client):
        """测试处理SERVER_ACK响应"""
        # 创建模拟对象
        mock_audio_device_instance = MagicMock()
        mock_audio_device_manager.return_value = mock_audio_device_instance
        mock_client_instance = MagicMock()
        mock_realtime_client.return_value = mock_client_instance
        
        # 创建DialogSession实例
        session = DialogSession(self.ws_config)
        
        # 创建模拟的SERVER_ACK响应
        response = {
            'message_type': 'SERVER_ACK',
            'payload_msg': b'test_audio_data'
        }
        
        # 调用处理方法
        session.handle_server_response(response)
        
        # 验证音频数据被放入队列
        self.assertFalse(session.audio_queue.empty())
        
    @patch('audio_manager.RealtimeDialogClient')
    @patch('audio_manager.AudioDeviceManager')
    def test_handle_server_response_full_response(self, mock_audio_device_manager, mock_realtime_client):
        """测试处理SERVER_FULL_RESPONSE响应"""
        # 创建模拟对象
        mock_audio_device_instance = MagicMock()
        mock_audio_device_manager.return_value = mock_audio_device_instance
        mock_client_instance = MagicMock()
        mock_realtime_client.return_value = mock_client_instance
        
        # 创建DialogSession实例
        session = DialogSession(self.ws_config)
        
        # 创建模拟的SERVER_FULL_RESPONSE响应 (event=450)
        response = {
            'message_type': 'SERVER_FULL_RESPONSE',
            'event': 450,
            'session_id': 'test_session_id',
            'payload_msg': {}
        }
        
        # 调用处理方法
        session.handle_server_response(response)
        
        # 验证状态变化
        self.assertTrue(session.is_user_querying)

if __name__ == '__main__':
    unittest.main()