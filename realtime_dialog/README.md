# RealtimeDialog

实时语音对话程序，支持语音输入和语音输出。

## 功能特性

- 实时语音识别和语音合成
- 支持与豆包大模型进行对话
- 音频输入输出管理
- WebSocket协议通信

## 系统要求

- Python 3.7 或更高版本
- 支持麦克风和扬声器的音频设备
- 网络连接

## 安装说明

### 1. 克隆项目

```bash
git clone <项目地址>
cd realtime_dialog
```

### 2. 创建虚拟环境（推荐）

```bash
# 使用uv创建虚拟环境
uv venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. 安装依赖

```bash
# 使用uv安装依赖（推荐）
uv pip install -r requirements.txt

# 或者使用pip安装
pip install -r requirements.txt
```

## 配置说明

1. 配置API密钥
   - 打开 `config.py` 文件
   - 修改以下两个字段：
     ```python
     "X-Api-App-ID": "火山控制台上端到端大模型对应的App ID",
     "X-Api-Access-Key": "火山控制台上端到端大模型对应的Access Key",
     ```

2. 可选配置
   - 根据需要调整音频参数（采样率、通道数等）
   - 修改对话角色名称和系统提示词

## 使用方法

运行程序：

```bash
python main.py
```

程序启动后：
1. 麦克风将自动开始录制
2. 对着麦克风说话即可与豆包对话
3. 程序会播放豆包的语音回复
4. 按 `Ctrl+C` 结束对话

## 项目结构

```
realtime_dialog/
├── audio_manager.py       # 音频设备管理和对话会话处理
├── config.py             # 配置文件
├── main.py               # 程序入口
├── protocol.py           # 协议处理模块
├── realtime_dialog_client.py  # WebSocket客户端
├── requirements.txt      # 依赖列表
└── tests/                # 单元测试
    ├── test_audio_manager.py
    ├── test_config.py
    ├── test_main.py
    ├── test_protocol.py
    └── test_realtime_dialog_client.py
```

## 测试

运行单元测试：

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试文件
python -m pytest tests/test_protocol.py -v
```

## 注意事项

1. 此demo使用python3.7环境进行开发调试，其他python版本可能会有兼容性问题，需要自己尝试解决。
2. 确保麦克风和扬声器正常工作
3. 网络连接稳定以保证实时对话体验
4. 在公共场所使用时请注意音量控制

## 故障排除

1. 如果遇到音频设备问题：
   - 检查麦克风和扬声器是否正常工作
   - 确认没有其他程序占用音频设备

2. 如果遇到连接问题：
   - 检查API密钥配置是否正确
   - 确认网络连接正常
   - 检查防火墙设置

3. 如果遇到依赖安装问题：
   - 尝试使用虚拟环境隔离依赖
   - 确保pip版本是最新的

## 许可证

[请在此处添加许可证信息]