import asyncio
import json
import threading
from audio_capture import AudioCapture
from doubao_client import DoubaoTranslationClient
from config import DOUBAO_CONFIG, AUDIO_CONFIG

class VideoTranslator:
    """英文视频同声传译器"""
    
    def __init__(self):
        self.audio_capture = AudioCapture(
            sample_rate=AUDIO_CONFIG["sample_rate"],
            channels=AUDIO_CONFIG["channels"],
            chunk_size=AUDIO_CONFIG["chunk_size"]
        )
        self.translation_client = DoubaoTranslationClient(DOUBAO_CONFIG)
        self.is_translating = False
        self.translation_thread = None
        
    async def start_translation(self, device_index=None):
        """开始同声传译"""
        if self.is_translating:
            print("翻译已在进行中...")
            return
            
        print("正在启动同声传译...")
        
        # 显示可用设备
        self.audio_capture.list_audio_devices()
        
        # 连接到豆包服务
        connected = await self.translation_client.connect()
        if not connected:
            print("无法连接到翻译服务，请检查配置")
            return
            
        # 开始音频捕获
        self.audio_capture.start_capture(device_index)
        self.is_translating = True
        
        print("同声传译已启动！正在监听英文音频并翻译为中文...")
        print("按 Ctrl+C 停止")
        
        try:
            await self._translation_loop()
        except KeyboardInterrupt:
            print("\n正在停止翻译...")
        finally:
            await self.stop_translation()
    
    async def _translation_loop(self):
        """翻译主循环"""
        while self.is_translating:
            try:
                # 获取音频数据
                audio_data = self.audio_capture.get_audio_data(timeout=0.1)
                if audio_data:
                    # 发送音频到翻译服务
                    await self.translation_client.send_audio(audio_data)
                
                # 接收翻译结果
                result = await self.translation_client.receive_translation()
                if result:
                    self._handle_translation_result(result)
                    
            except Exception as e:
                print(f"翻译循环错误: {e}")
                await asyncio.sleep(0.1)
    
    def _handle_translation_result(self, result: dict):
        """处理翻译结果"""
        if isinstance(result, dict):
            # 处理不同类型的结果
            if "asr" in result:
                asr_text = result["asr"].get("text", "")
                if asr_text:
                    print(f"识别: {asr_text}")
            
            if "translation" in result:
                translation_text = result["translation"].get("text", "")
                if translation_text:
                    print(f"翻译: {translation_text}")
            
            if "tts" in result:
                # 这里可以处理TTS音频播放
                pass
        else:
            # 直接打印文本结果
            print(f"翻译结果: {result}")
    
    async def stop_translation(self):
        """停止翻译"""
        self.is_translating = False
        self.audio_capture.stop_capture()
        await self.translation_client.close()
        print("同声传译已停止")
    
    def run(self):
        """运行翻译器"""
        try:
            asyncio.run(self.start_translation())
        except KeyboardInterrupt:
            print("\n程序被用户中断")

if __name__ == "__main__":
    translator = VideoTranslator()
    translator.run()