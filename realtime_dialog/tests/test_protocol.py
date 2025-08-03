import sys
import os
import unittest
import gzip
from unittest.mock import patch, MagicMock, AsyncMock

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from protocol import generate_header, parse_response, PROTOCOL_VERSION, CLIENT_FULL_REQUEST, \
    MSG_WITH_EVENT, JSON, GZIP, NO_COMPRESSION, SERVER_FULL_RESPONSE, SERVER_ACK, SERVER_ERROR_RESPONSE

class TestProtocol(unittest.TestCase):
    """测试protocol.py模块"""

    def test_generate_header(self):
        """测试生成协议头"""
        header = generate_header()
        self.assertIsInstance(header, bytearray)
        self.assertEqual(len(header), 4)  # 默认头部大小为4字节
        
        # 测试自定义参数
        custom_header = generate_header(
            version=2,
            message_type=2,
            message_type_specific_flags=2,
            serial_method=2,
            compression_type=2
        )
        self.assertEqual(custom_header[0] >> 4, 2)  # 版本号
        self.assertEqual(custom_header[1] >> 4, 2)  # 消息类型
        self.assertEqual(custom_header[2] >> 4, 2)  # 序列化方法
        
    def test_parse_response_with_empty_string(self):
        """测试解析空字符串响应"""
        result = parse_response("")
        self.assertEqual(result, {})
        
    def test_parse_response_server_full_response(self):
        """测试解析SERVER_FULL_RESPONSE类型的响应"""
        # 构造一个模拟的SERVER_FULL_RESPONSE响应
        header = generate_header(
            message_type=SERVER_FULL_RESPONSE,
            message_type_specific_flags=MSG_WITH_EVENT,
            serial_method=JSON,
            compression_type=GZIP
        )
        
        # 添加事件、会话ID和负载数据
        payload_data = b'{"test": "data"}'
        compressed_payload = gzip.compress(payload_data)
        
        # 构建完整响应
        response = bytearray(header)
        response.extend((450).to_bytes(4, 'big'))  # 事件
        response.extend((len("test_session_id")).to_bytes(4, 'big'))  # 会话ID长度
        response.extend(b"test_session_id")  # 会话ID
        response.extend((len(compressed_payload)).to_bytes(4, 'big'))  # 负载大小
        response.extend(compressed_payload)  # 压缩的负载数据
        
        result = parse_response(bytes(response))
        self.assertEqual(result['message_type'], 'SERVER_FULL_RESPONSE')
        self.assertEqual(result['event'], 450)
        self.assertEqual(result['session_id'], "b'test_session_id'")
        self.assertEqual(result['payload_msg'], {"test": "data"})
        
    def test_parse_response_server_ack(self):
        """测试解析SERVER_ACK类型的响应"""
        # 构造一个模拟的SERVER_ACK响应
        header = generate_header(
            message_type=SERVER_ACK,
            message_type_specific_flags=0,  # 不带事件
            serial_method=JSON,
            compression_type=NO_COMPRESSION  # 不压缩
        )
        
        # 添加会话ID和负载数据
        payload_data = b'{"ack": "data"}'
        
        # 构建完整响应
        response = bytearray(header)
        response.extend((len("test_session_id")).to_bytes(4, 'big'))  # 会话ID长度
        response.extend(b"test_session_id")  # 会话ID
        response.extend((len(payload_data)).to_bytes(4, 'big'))  # 负载大小
        response.extend(payload_data)  # 负载数据
        
        result = parse_response(bytes(response))
        self.assertEqual(result['message_type'], 'SERVER_ACK')
        self.assertEqual(result['session_id'], "b'test_session_id'")
        self.assertEqual(result['payload_msg'], {"ack": "data"})
        
    def test_parse_response_server_error(self):
        """测试解析SERVER_ERROR_RESPONSE类型的响应"""
        # 构造一个模拟的SERVER_ERROR_RESPONSE响应
        header = generate_header(
            message_type=SERVER_ERROR_RESPONSE,
            message_type_specific_flags=0,
            serial_method=JSON,
            compression_type=GZIP
        )
        
        # 添加错误码和负载数据
        payload_data = b'{"error": "something went wrong"}'
        compressed_payload = gzip.compress(payload_data)
        
        # 构建完整响应
        response = bytearray(header)
        response.extend((500).to_bytes(4, 'big'))  # 错误码
        response.extend((len(compressed_payload)).to_bytes(4, 'big'))  # 负载大小
        response.extend(compressed_payload)  # 压缩的负载数据
        
        result = parse_response(bytes(response))
        self.assertEqual(result['code'], 500)
        self.assertEqual(result['payload_msg'], {"error": "something went wrong"})

if __name__ == '__main__':
    unittest.main()