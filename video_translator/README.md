# 英文视频同声传译工具

这是一个基于豆包实时语音API的英文视频同声传译MVP工具，可以将播放的英文视频实时翻译成中文。

## 功能特点

- 🎤 实时捕获系统音频输入
- 🌐 支持英文到中文的实时翻译
- 🔊 基于豆包语音大模型的翻译服务
- ⚡ 低延迟同声传译
- 🖥️ Windows平台支持

## 安装

### 使用 uv 安装

1. 安装 uv（如果尚未安装）：
```bash
pip install uv
```

2. 创建虚拟环境并安装依赖：
```bash
uv venv
uv pip install -r requirements.txt
```

### 使用 pip 安装

```bash
pip install -r requirements.txt
```

## 配置

编辑 `config.py` 文件，设置你的豆包API凭证：

```python
DOUBAO_CONFIG = {
    "base_url": "wss://openspeech.bytedance.com/api/v3/realtime/dialogue",
    "headers": {
        "X-Api-App-ID": "你的APP-ID",
        "X-Api-Access-Key": "你的ACCESS-KEY",
        # ... 其他配置保持不变
    }
}
```

## 使用方法

1. **启动程序**：
```bash
python translator.py
```

2. **选择音频设备**：
   程序启动时会显示可用的音频输入设备列表，选择你想要捕获的设备索引

3. **播放英文视频**：
   在电脑上播放任何英文视频内容

4. **实时翻译**：
   程序会自动捕获英文音频并实时翻译成中文文本输出

5. **停止程序**：
   按 `Ctrl+C` 停止翻译

## 音频设备配置

### Windows 音频捕获设置

1. **立体声混音**：
   - 右键点击系统音量图标 → 声音设置
   - 点击"声音控制面板"
   - 选择"录制"标签页
   - 启用"立体声混音"（Stereo Mix）
   - 将其设置为默认设备

2. **虚拟音频设备**（推荐）：
   - 安装 [VB-Cable](https://vb-audio.com/Cable/index.htm)
   - 将系统音频输出设置为 VB-Cable Input
   - 程序将捕获 VB-Cable Output 作为输入源

## 常见问题

### 1. 找不到音频设备
- 确保已启用立体声混音或安装了虚拟音频设备
- 检查音频驱动是否正常

### 2. API连接失败
- 检查网络连接
- 验证API凭证是否正确
- 确保API服务已开通

### 3. 翻译延迟过高
- 检查网络延迟
- 尝试降低音频采样率
- 确保系统性能充足

## 项目结构

```
video_translator/
├── translator.py          # 主程序
├── audio_capture.py       # 音频捕获模块
├── doubao_client.py       # 豆包API客户端
├── config.py             # 配置文件
├── pyproject.toml        # 项目配置
└── README.md            # 说明文档
```

## 技术栈

- **音频处理**：PyAudio
- **网络通信**：websockets
- **API集成**：豆包实时语音API
- **异步处理**：asyncio
- **依赖管理**：uv/pip

## 注意事项

1. **API配额**：豆包API有使用限制，请注意配额管理
2. **网络要求**：需要稳定的网络连接以获得最佳体验
3. **隐私保护**：音频数据会发送到豆包服务器进行处理
4. **系统权限**：可能需要管理员权限访问音频设备

## 扩展功能

未来可以添加的功能：
- 支持更多语言对
- 实时语音合成输出
- 翻译结果保存到文件
- 图形用户界面
- 翻译质量优化

## 支持

如有问题，请检查：
1. 音频设备配置是否正确
2. API凭证是否有效
3. 网络连接是否稳定
4. 查看控制台输出获取详细错误信息