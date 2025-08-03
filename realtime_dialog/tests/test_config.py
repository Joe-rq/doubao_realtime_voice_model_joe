import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config

class TestConfig(unittest.TestCase):
    """测试config.py模块"""

    def test_ws_connect_config_exists(self):
        """测试ws_connect_config配置存在"""
        self.assertTrue(hasattr(config, 'ws_connect_config'))
        self.assertIsInstance(config.ws_connect_config, dict)
        self.assertIn('base_url', config.ws_connect_config)
        self.assertIn('headers', config.ws_connect_config)
        
    def test_ws_connect_config_headers(self):
        """测试WebSocket连接配置的头部信息"""
        headers = config.ws_connect_config['headers']
        self.assertIn('X-Api-App-ID', headers)
        self.assertIn('X-Api-Access-Key', headers)
        self.assertIn('X-Api-Resource-Id', headers)
        self.assertIn('X-Api-App-Key', headers)
        self.assertIn('X-Api-Connect-Id', headers)
        
        # 检查固定值
        self.assertEqual(headers['X-Api-Resource-Id'], "volc.speech.dialog")
        self.assertEqual(headers['X-Api-App-Key'], "PlgvMymc7f3tQnJ6")
        
    def test_start_session_req_exists(self):
        """测试start_session_req配置存在"""
        self.assertTrue(hasattr(config, 'start_session_req'))
        self.assertIsInstance(config.start_session_req, dict)
        self.assertIn('tts', config.start_session_req)
        self.assertIn('dialog', config.start_session_req)
        
    def test_start_session_req_tts(self):
        """测试start_session_req中的TTS配置"""
        tts_config = config.start_session_req['tts']
        self.assertIn('audio_config', tts_config)
        audio_config = tts_config['audio_config']
        self.assertEqual(audio_config['channel'], 1)
        self.assertEqual(audio_config['format'], "pcm")
        self.assertEqual(audio_config['sample_rate'], 24000)
        
    def test_start_session_req_dialog(self):
        """测试start_session_req中的对话配置"""
        dialog_config = config.start_session_req['dialog']
        self.assertIn('bot_name', dialog_config)
        self.assertIn('system_role', dialog_config)
        self.assertIn('speaking_style', dialog_config)
        self.assertIn('extra', dialog_config)
        
    def test_input_audio_config_exists(self):
        """测试input_audio_config配置存在"""
        self.assertTrue(hasattr(config, 'input_audio_config'))
        self.assertIsInstance(config.input_audio_config, dict)
        required_keys = ['chunk', 'format', 'channels', 'sample_rate', 'bit_size']
        for key in required_keys:
            self.assertIn(key, config.input_audio_config)
            
    def test_output_audio_config_exists(self):
        """测试output_audio_config配置存在"""
        self.assertTrue(hasattr(config, 'output_audio_config'))
        self.assertIsInstance(config.output_audio_config, dict)
        required_keys = ['chunk', 'format', 'channels', 'sample_rate', 'bit_size']
        for key in required_keys:
            self.assertIn(key, config.output_audio_config)

if __name__ == '__main__':
    unittest.main()