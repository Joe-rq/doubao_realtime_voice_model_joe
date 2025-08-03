import pyaudio
import numpy as np
import threading
import queue
import time
from typing import Optional

class AudioCapture:
    """系统音频捕获类"""
    
    def __init__(self, sample_rate=16000, channels=1, chunk_size=1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format = pyaudio.paInt16
        
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.thread = None
        
    def list_audio_devices(self):
        """列出所有音频输入设备"""
        print("可用的音频输入设备:")
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"  {i}: {info['name']} - 输入通道数: {info['maxInputChannels']}")
    
    def start_capture(self, device_index=None):
        """开始捕获音频"""
        if self.is_recording:
            return
            
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=self.chunk_size
        )
        
        self.is_recording = True
        self.thread = threading.Thread(target=self._capture_loop)
        self.thread.daemon = True
        self.thread.start()
        print("音频捕获已启动")
    
    def stop_capture(self):
        """停止捕获音频"""
        self.is_recording = False
        if self.thread:
            self.thread.join()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        print("音频捕获已停止")
    
    def _capture_loop(self):
        """音频捕获循环"""
        while self.is_recording:
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                self.audio_queue.put(data)
            except Exception as e:
                print(f"音频捕获错误: {e}")
                break
    
    def get_audio_data(self, timeout=1.0):
        """获取音频数据"""
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def has_audio_data(self):
        """检查是否有音频数据"""
        return not self.audio_queue.empty()
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'audio'):
            self.audio.terminate()