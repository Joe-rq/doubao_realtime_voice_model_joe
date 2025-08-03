import asyncio
import websockets
import json
import gzip
import uuid
from typing import Dict, Any, Optional

class DoubaoTranslationClient:
    """豆包实时翻译客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session_id = str(uuid.uuid4())
        self.ws = None
        self.logid = ""
        self.is_connected = False
        
    async def connect(self) -> bool:
        """建立WebSocket连接"""
        try:
            print(f"连接到豆包服务器: {self.config['base_url']}")
            self.ws = await websockets.connect(
                self.config['base_url'],
                extra_headers=self.config['headers'],
                ping_interval=None
            )
            
            self.logid = self.ws.response_headers.get("X-Tt-Logid")
            print(f"连接成功，logid: {self.logid}")
            
            # 发送开始连接请求
            await self._send_start_connection()
            
            # 发送开始会话请求
            await self._send_start_session()
            
            self.is_connected = True
            return True
            
        except Exception as e:
            print(f"连接失败: {e}")
            return False
    
    async def _send_start_connection(self):
        """发送开始连接请求"""
        header = bytearray([0x11, 0x10, 0x11, 0x00])
        request = bytearray()
        request.extend(header)
        request.extend((1).to_bytes(4, 'big'))  # 消息类型
        
        payload = json.dumps({})
        compressed = gzip.compress(payload.encode())
        request.extend(len(compressed).to_bytes(4, 'big'))
        request.extend(compressed)
        
        await self.ws.send(request)
        response = await self.ws.recv()
        print("开始连接响应已接收")
    
    async def _send_start_session(self):
        """发送开始会话请求"""
        session_config = {
            "asr": {
                "enable": True,
                "language": "en-US",
                "enable_punctuation": True,
                "enable_interim_results": True
            },
            "tts": {
                "enable": True,
                "language": "zh-CN",
                "voice_type": "xiaoyun",
                "speed": 1.0,
                "volume": 1.0,
                "pitch": 1.0
            },
            "translation": {
                "enable": True,
                "from": "en",
                "to": "zh"
            }
        }
        
        header = bytearray([0x11, 0x10, 0x11, 0x00])
        request = bytearray()
        request.extend(header)
        request.extend((100).to_bytes(4, 'big'))  # 消息类型
        request.extend(len(self.session_id).to_bytes(4, 'big'))
        request.extend(self.session_id.encode())
        
        payload = json.dumps(session_config)
        compressed = gzip.compress(payload.encode())
        request.extend(len(compressed).to_bytes(4, 'big'))
        request.extend(compressed)
        
        await self.ws.send(request)
        response = await self.ws.recv()
        print("开始会话响应已接收")
    
    async def send_audio(self, audio_data: bytes):
        """发送音频数据"""
        if not self.is_connected or not self.ws:
            return
            
        try:
            header = bytearray([0x11, 0x10, 0x11, 0x00])
            request = bytearray()
            request.extend(header)
            request.extend((2).to_bytes(4, 'big'))  # 音频数据消息类型
            request.extend(audio_data)
            
            await self.ws.send(request)
        except Exception as e:
            print(f"发送音频数据失败: {e}")
    
    async def receive_translation(self) -> Optional[Dict[str, Any]]:
        """接收翻译结果"""
        if not self.is_connected or not self.ws:
            return None
            
        try:
            response = await self.ws.recv()
            if isinstance(response, bytes):
                # 简单的响应解析
                try:
                    text = response.decode('utf-8')
                    return json.loads(text)
                except:
                    return None
            elif isinstance(response, str):
                return json.loads(response)
        except Exception as e:
            print(f"接收翻译结果失败: {e}")
            return None
    
    async def close(self):
        """关闭连接"""
        if self.ws:
            await self.ws.close()
            self.is_connected = False
            print("连接已关闭")