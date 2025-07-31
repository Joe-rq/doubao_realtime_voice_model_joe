# 端到端实时语音大模型API接入文档--豆包语音-火山引擎

---

- 端到端实时语音大模型API接入文档--豆包语音-火山引擎
- [https://www.volcengine.com/docs/6561/1594356](https://www.volcengine.com/docs/6561/1594356)
- 火山引擎官方文档中心，产品文档、快速入门、用户指南等内容，你关心的都在这里，包含火山引擎主要产品的使用手册、API或SDK手册、常见问题等必备资料，我们会不断优化，为用户带来更好的使用体验
- 2025-07-30 15:15

---

端到端实时语音大模型API接入文档

最近更新时间：2025.07.14 17:00:33首次发布时间：2025.06.11 14:22:46

1 接口功能

豆包端到端实时语音大模型API即RealtimeAPI支持低延迟、多模式交互，可用于构建语音到语音的对话工具。该API支持中文和英语两大语种，目前只支持WebSocket协议连接到此API，同时支持客户边发送数据边接收数据的流式交互方式。

## 1. 产品约束

1. 客户端上传音频格式要求PCM（脉冲编码调制，未经压缩的的音频格式）、单声道、采样率16000、每个采样点用`int16`表示、字节序为小端序。
2. 服务端返回的是 OGG 封装的 Opus 音频，兼顾压缩效率与传输性能。
3. 若客户端在 StartSession事件中增加TTS配置，服务端可返回 PCM 格式的音频流（单声道、24000Hz 采样率、Float32 采样点、小端序）。具体请求参数如下所示：

```JSON
{
    "tts" : {
        "audio_config": {
            "channel": 1,
            "format": "pcm",
            "sample_rate": 24000
        }
    }
}
JSON
```

4. 限流条件分为QPM和TPM，QPM全称query per minute，这里的query对应StartSession事件，即在一个AppID下面每分钟的StartSession事件不能超过配额值。TPM全称tokens per minute，即一分钟所消耗的全部token不能超过对应的配额值。

## 2. 最佳实践

1. 实时对话采用流式输入输出架构，即便用户未发起 query，客户端也需持续发送音频，以维持流式处理链路的正常运行。
2. 在客户端发送 FinishSession 事件后，系统将不再返回任何事件。但客户端仍可复用与火山语音网关之间的 WebSocket 连接。若需发起新的会话，客户端需重新从 StartSession 事件开始。

![Image](assets/792768cc8d2f4be7b74cae61b9f1b722tplv-goo7wpa0wc-image.image-20250730151503-kn8hpfa.png)

3. 在没有对话需求时候，可以发送FinishSession事件结束会话。如果不想复用websocket连接，可以继续发送FinishConnection事件，释放对应的websocket连接。
4. 推荐客户端在事件的 optional 字段中携带 event 和 session ID，以降低开发成本，并将事件处理的复杂性交由火山语音服务端负责。
5. 客户在集成端到端语音合成模型过程中，使用 ChatTTSText 进行音频合成请求的最佳实践方法，其中黄色部分需要客户实现：

![Image](assets/e00fc94e88ca485ab8a8b2c107552ed3tplv-goo7wpa0wc-image.image-20250730151503-3a0frnh.png)

2 接口说明

WebSocket是一种广泛支持的实时数据传输API，也是服务器应用程序中连接到豆包端到端实时语音大模型API的最佳选择。在客户服务器上集成此API时候，可以通过WebSocket直接连接到实时语音大模型API，具体鉴权参数可以在火山控制台获取。

## 3. ws连接详细信息

- 通过WebSocket建立连接需要以下连接信息：

|URL|wss://openspeech.bytedance.com/api/v3/realtime/dialogue||||
| -------------------| ---------------------------------------------------------------| ------| --------------------------------------| -----------|
|Request Headers|Key|说明|是否必须|Value示例|
|X-Api-App-ID|使用火山引擎控制台获取的APP ID，可参考[控制台使用FAQ-Q1](https://www.volcengine.com/docs/6561/196768#q1%EF%BC%9A%E5%93%AA%E9%87%8C%E5%8F%AF%E4%BB%A5%E8%8E%B7%E5%8F%96%E5%88%B0%E4%BB%A5%E4%B8%8B%E5%8F%82%E6%95%B0appid%EF%BC%8Ccluster%EF%BC%8Ctoken%EF%BC%8Cauthorization-type%EF%BC%8Csecret-key-%EF%BC%9F)|是|123456789||
|X-Api-Access-Key|使用火山引擎控制台获取的Access Token，可参考[控制台使用FAQ-Q1](https://www.volcengine.com/docs/6561/196768#q1%EF%BC%9A%E5%93%AA%E9%87%8C%E5%8F%AF%E4%BB%A5%E8%8E%B7%E5%8F%96%E5%88%B0%E4%BB%A5%E4%B8%8B%E5%8F%82%E6%95%B0appid%EF%BC%8Ccluster%EF%BC%8Ctoken%EF%BC%8Cauthorization-type%EF%BC%8Csecret-key-%EF%BC%9F)|是|your-access-key||
|X-Api-Resource-Id|表示调用服务的资源信息 ID<br />固定值：volc.speech.dialog|是|volc.speech.dialog||
|X-Api-App-Key|固定值|是|PlgvMymc7f3tQnJ6||
|X-Api-Connect-Id|用于追踪当前连接情况的标志 ID<br />建议用户传递，便于排查连接情况|否|d1dcd999-9a9e-4ed6-b227-8649e946f6c4||

- 在 websocket 握手成功后，会返回如下Response header

|Key|说明|Value示例|
| ------------| ----------------------------------------------------| ------------------------------------|
|X-Tt-Logid|服务端返回的 logid，建议用户获取和打印方便定位问题|20250506234111719BC62BBA7C4C0C635A|

## 4. WebSocket二进制协议

豆包端到端实时语音大模型API使用二进制协议传输数据，协议由4字节的header、optioanl、payload size和payload三部分组成，其中：

- header用于描述消息类型、序列化方式以及压缩格式等信息
- optional可选字段

  - sequence字段
  - event字段，用于描述链接过程中状态管理的预定义事件
  - connect id size/ connect id字段，用于描述连接类事件的标识
  - session id size/ session id 字段，用于描述会话类事件的标识
  - error code: 仅用于错误帧，描述错误信息
- payload size代表payload的长度
- payload是具体负载的内容，依据不同的消息类型装载不同的内容

|Byte|Left-4bit|Right-4bit|说明|
| ------| ----------------------| -------------------------------------------------------------------------------| -----------------------------------------------------------------------------------------------|
|0|Protocol Version||目前只有v1，固定0b0001|
||Header Size|目前只有4字节固定0b0001||
|1|Message Type|Message type specific flags|详细见下面消息说明|
|2|Serialization method||- 0b0000：Raw（无特殊序列化，主要针对二进制音频数据）<br />- 0b0001：JSON（主要针对文本类型消息）|
||Compression method|- 0b0000：无压缩（​\<strong\>推荐\</strong\>）<br />- 0b0001：gzip||
|3|0x00|Reserved||

#### 4.0.1 Mesage Type

|Message Type|含义|说明|
| --------------| ----------------------| --------------------------------|
|0b0001|Full-client request|客户端发送文本事件的消息类型|
|0b1001|Full-server response|服务器返回的文本事件的消息类型|
|0b0010|Audio-only request|客户端发送音频数据的消息类型|
|0b1011|Audio-only response|服务器返回音频数据的消息类型|
|0b1111|Error information|服务器返回的错误事件的消息类型|

### 4.1 Message type specific flags

Optional可选字段code、sequence、event取决于Message type specific flags，而connect id和session id取决于事件类型。如果设置对应flag请**按照表格顺序**进行二进制组装。目前支持的全集如下所示：

|字段|长度（Byte）|说明|Message type specific flags|
| -----------------| -----------------------| -----------------------------------------------------------------------------| --------------------------------------------------------------------------------------------------------------------------------------------------------|
|code|4|【可选】错误码code|- 0b1111：错误帧|
|sequence|4|【可选】描述客户端的事件序号|- 0b0000：没有sequence字段<br />- 0b0001：序号大于 0 的非终端数据包<br />- 0b0010：最后一个无序号的数据包<br />- 0b0011：最后一个序号小于 0 的数据包，一般用-1表示|
|event|4|【必须】描述连接过程中状态管理的预定义事件，详细参考[实时对话事件](https://www.volcengine.com/docs/6561/1594356#_2-3-%E5%AE%9E%E6%97%B6%E5%AF%B9%E8%AF%9D%E4%BA%8B%E4%BB%B6)中的事件ID|- 0b0100：携带事件ID|
|connect id size|4|【可选】客户事件携带的connect id对应的长度，只有Connect事件才能携带此字段|——|
|connect id|取决于connect id size|【可选】客户生成的connect id||
|session id size|4|【必须】客户事件携带的session id对应的长度，只有Session级别的事件携带此字段||
|session id|取决于session id size|【必须】客户事件携带的session id||

### 4.2 具体的payload size和payload

payload可以放音频二进制数据，也可以放类似StartSession事件中的json数据。

|字段|长度（Byte）|说明|
| --------------| ------------------------| -------------------------------------------------------|
|payload size|4|paylaod长度|
|payload|长度取决于payload size|payload内容，可以是二进制音频数据，也可以是json字符串|

#### 4.2.1 错误帧payload

```Plain
{
    "error": {{STRING}}
}
Plain
```

## 5. 实时对话事件

通过WebSocket连接到豆包端到端实时语音大模型API之后，可以调用`S2S模型`进行语音到语音的对话。需要**发送客户端事件**来启动操作，并**监听服务器事件**以采取对应的操作。

### 5.1 客户端事件

|事件ID|事件定义|事件类型|说明|示例|
| --------| ------------------| ----------------------------------------------------------------------------------------------| -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------------------------------------------------------|
|1|StartConnection|Connect类事件|Websocket 阶段申明创建连接|​`{}`​<br />`JSON`​|
|2|FinishConnection|断开websocket连接，后面需要重新发起websocket连接|||
|100|StartSession|Session类事件|Websocket 阶段申明创建会话，其中：- bot\\\_name字段用于修改基础人设信息，例如人名、来源等，默认为豆包<br />- system\\\_role字段用于配置背景人设信息，描述角色的来源、设定等，例如“你是大灰狼、用户是小红帽，用户逃跑时你会威胁吃掉他。”<br />- speaking\\\_style字段用于配置模型对话风格，例如“你说话偏向林黛玉。”、“你口吻拽拽的。”等<br />- 长度限制：bot\\\_name 最长不超过 20 个字符，system\\\_role 与 speaking\\\_style 合计不得超过 1500 个字符<br />- dialog\\\_id字段用于加载相同dialog id的session对话记录，进而提升模型回复能力<br />- strict\\\_audit字段用于声明安全审核等级，true代表严格审核、false代表普通审核，默认为true<br />- audit\\\_response字段用于指定用户query命中安全审核之后的自定义回复话术|​`{`​<br />`    "dialog": {`​<br />`        "bot_name": {{STRING}},`​<br />`        "system_role": {{STRING}},`​<br />`        "speaking_style": {{STRING}},`​<br />`        "dialog_id": {{STRING}},`​<br />`        "extra" : {`​<br />`            "strict_audit": {{BOOLEAN}},`​<br />`            "audit_response": {{STRING}}`​<br />`        }`​<br />`    }`​<br />`}`​<br />`JSON`​|
|102|FinishSession|客户端声明结束会话，后面可以复用websocket连接|​`{}`​<br />`JSON`​||
|200|TaskRequest|客户端上传音频|音频二进制数据||
|300|SayHello|客户端提交打招呼文本|​`{`​<br />`    "content": {{STRING}}`​<br />`}`​<br />`JSON`​||
|500|ChatTTSText|用户query之后，模型会生成闲聊结果。如果客户判断用户query不需要闲聊结果，可以指定文本合成音频|​`{`​<br />`    "start": {{BOOLEAN}},`​<br />`    "content": {{STRING}},`​<br />`    "end": {{BOOLEAN}}`​<br />`}`​<br />`Plain`​||

备注：

- Websocket阶段：在 HTTP 建立连接之后Upgrade
- 客户端在发送FinishSession事件之后，websocket连接不会断开，客户端可以继续复用，复用时候需要再发送一次StartSession事件，即重新初始化会话
- Message Type \= 0b0001，Message type specific flags \= 0b0100，StartConnection事件二进制帧对应的字节数组示例：

  - [17 20 16 0 0 0 0 1 0 0 0 2 123 125]
- Message Type \= 0b0001，Message type specific flags \= 0b0100，SessionID \= 75a6126e-427f-49a1-a2c1-621143cb9db3，jsonPayload \= {"dialog":{"bot\_name":"豆包","dialog\_id":"","extra":null}}，StartSession事件二进制帧对应的字节数组示例：

```Plain
[17 20 16 0 0 0 0 100 0 0 0 36 55 53 97 54 49 50 54 101 45 52 50 55 102 45 52 57 97 49 45 97 50 99 49 45 54 50 49 49 52 51 99 98 57 100 98 51 0 0 0 60 123 34 100 105 97 108 111 103 34 58 123 34 98 111 116 95 110 97 109 101 34 58 34 232 177 134 229 140 133 34 44 34 100 105 97 108 111 103 95 105 100 34 58 34 34 44 34 101 120 116 114 97 34 58 110 117 108 108 125 125]
Plain
```

- ChatTTSText事件请求示例：

  - 第一包json示例

```Plain
{
    "start": true,
    "content": "今天是",
    "end": false
}
Plain
```

- 中间包，用于流式上传待合成音频的文本

```Plain
{
    "start": false,
    "content": "星期二。",
    "end": false
}
Plain
```

- 最后一包，若在音频播报过程中发起新的 query 导致中断，且合成音频的 end 包尚未发送，此时无需再下发该 end 包，以避免多余流程或状态异常。

```JSON
{
    "start": false,
    "content": "",
    "end": true
}
JSON
```

### 5.2 服务端事件

|事件ID|事件定义|事件类型|说明|示例|
| --------| --------------------| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ---------------------------------------------------------------------| ------------------|
|50|ConnectionStarted|Connect类|成功建立连接|​`{}`​<br />`JSON`​|
|51|ConnectionFailed|建立连接失败|​`{`​<br />`    "error": {{STRING}}`​<br />`}`​<br />`JSON`​||
|52|ConnectionFinished|连接结束|​`{}`​<br />`JSON`​||
|150|SessionStarted|Session类|成功启动会话，返回的dialog id用于接续最近的对话内容，增加模型智能度|​`{`​<br />`    "dialog_id": {{STRING}}`​<br />`}`​<br />`JSON`​|
|152|SessionFinished|会话已结束|​`{}`​<br />`JSON`​||
|153|SessionFailed|会话失败|​`{`​<br />`    "error": {{STRING}}`​<br />`}`​<br />`JSON`​||
|350|TTSSentenceStart|合成音频的起始事件，tts\_type取值类型有：- audit\\\_content\\\_risky（命中安全审核音频）<br />- chat\\\_tts\\\_text（客户文本合成音频）<br />- default（闲聊音频）|​`{`​<br />`    "tts_type": {{STRING}},`​<br />`    "text" : {{STRING}},`​<br />`}`​<br />`JSON`​||
|351|TTSSentenceEnd|合成音频的分句结束事件|​`{}`​<br />`Shell`​||
|352|TTSResponse|返回模型生成的音频数据|payload装载二进制音频数据||
|359|TTSEnded|模型一轮音频合成结束事件|​`{}`​<br />`JSON`​||
|450|ASRInfo|模型识别出音频流中的首字返回的事件，用于打断客户端的播报|||
|451|ASRResponse|模型识别出用户说话的文本内容|​`{`​<br />`    "results": [`​<br />`      {`​<br />`        "text": {{STRING}},`​<br />`        "is_interim": {{BOOLEAN}}`​<br />`      }`​<br />`    ]`​<br />`}`​<br />`JSON`​||
|459|ASREnded|模型认为用户说话结束的事件|​`{}`​<br />`JSON`​||
|550|ChatResponse|模型回复的文本内容|​`{`​<br />`  "content": {{STRING}},`​<br />`}`​<br />`JSON`​||
|559|ChatEnded|模型回复文本结束事件|​`{}`​<br />`JSON`​||

备注：

- 服务器事件中json paylod可能会多返回一些字段，客户端无需关心
- Message type specific flags \= 0b0100，session id \=3c791a7d-227a-4446-993b-24f9e302cc98，TTSResponse事件示例：

  - [17 180 0 0 0 0 1 96 0 0 0 36 51 99 55 57 49 97 55 100 45 50 50 55 97 45 52 52 52 54 45 57 57 51 98 45 50 52 102 57 101 51 48 50 99 99 57 56 0 0 7 252 79 103 103 83 0 0 64 129 32 0 0 0 0 0 132 149 185 182 172 8 0 0 169 57 249 174 1 71 104 139 98 229 167 232 122 108 0 183 60 54 43 137 197 126 20 248 201 174]

3 快速开始

## 6. Python示例

![](assets/image-20250730151504-0d4a1mo.png)

realtime\_dialog.zip

未知大小

![](assets/image-20250730151504-f9svjjb.png)

## 7. Go示例

![](assets/image-20250730151504-tbgv0k8.png)

realtime\_dialog.zip

未知大小

![](assets/image-20250730151504-272l10o.png)

您可以通过以下步骤，快速体验与 Realtime 模型API实时对话的功能。

1. 下载realtime\_dialog.zip文件到本地，依据操作系统类型对`gordonklaus/portaudio`依赖进行安装：

    1. macOS：

```Bash
brew install portaudio
Bash
```

2. CentOS：

```Bash
sudo yum install -y portaudio portaudio-devel
Bash
```

3. Debian/Ubuntu：

```Shell
sudo apt-get install portaudio19-dev
Shell
```

2. 安装后在项目下运行：

```Shell
go执行命令：go run . -v=0
python执行命令：python main.py
Shell
```

4 交互示例

RealtimeAPI的交互流程目前只支持server\_vad模式，该模式的交互流程如下：

1. 客户端发送StartSession事件初始化会话
2. 客户端可以随时通过TaskRequest事件将音频发送到服务端
3. 服务端在检测到用户说话的时候，会返回ASRInfo和ASRResponse事件，同时在检测到用户说话结束之后返回ASREnded事件
4. 服务端合成的音频通过TTSResponse事件将音频返回给客户端

![Image](assets/48ba02413863450db726bd556e866981tplv-goo7wpa0wc-image.image-20250730151504-gteutez.png)

## 8. 合成音频

当客户判定不使用模型生成闲聊内容时，系统允许客户多次上传文本执行音频合成，以满足多样化需求。整体交互示例如下所示：  
​![Image](assets/f2a8516c2b6045f48890cbac1fc80ca6tplv-goo7wpa0wc-image.image-20250730151504-tzcou5b.png)

5 错误码

|类型|错误码|错误定义|说明|
| ---------------------------------------------------------| ------------------------| ------------------------------------| ---------------------------------------------------------------------------|
|客户端|45000002|Empty audio|客户上传空的音频包，即TaskRequest事件中的音频长度为0|
|45000003|Abnormal silence audio|10分钟静音释放链接||
|服务端|55000001|Server processing error|服务端超过10秒没有收到query音频（客户端想要保持链接需要一直发送静音音频）|
|下游服务超过35秒没有收到tts回复||||
|服务端处理错误（通用型错误，需要借助logid进行深入排查）||||
|55000030|Service unavailable|下游模块建立连接失败||
|55002070|AudioFlow error|下游返回错误信息，统一对外的错误码||

6.文档修订记录

|日期|update|
| ----------| ---------------------------------------------------------------------------------------------------------------------|
|25.07.14|支持客户自定义用户query命中安全审核时候的回复话术，新增audit\_response字段|
|25.07.09|go示例修复一个tts音色配置bug|
|25.07.03|python示例开放模型人设区域，提升端到端模型自定义能力；增加SayHello、ChatTTSText事件发送示例；|
|25.07.01|客户端在发送ChatTTSText事件时候一定要在收到ASREnded事件之后；增加一些报错处理，例如appkey错误、sp配置长度超过限制；|
|25.06.25|Go示例开放模型人设区域，提升端到端模型自定义能力；增加SayHello、ChatTTSText事件发送示例；|
|25.06.10|更新realtime\_dialog示例，用户query打断本地播放音频|
|25.06.05|更新realtime\_dialog 示例，ctrl+c之后发送FinishSession、FinishConnection事件之后，再调用close断开websocket连接|
|25.06.05|补充客户接入ChatTTSText的最佳实践|
|25.06.04|删除服务端返回的UsageResponse事件，客户可以在火山控制台查看用量|
|25.06.04|更新realtime\_dialog Go示例demo，新增sayHello、chatTTSTesxt数据构造示例|
|25.06.03|新增realtime\_dialog Python示例demo|
|25.05.30|更新realtime\_dialog示例，新增pcm保存到文件代码示例|
|25.05.30|更新Message type specific flags说明，注明必须传的字段|
|25.05.28|更新realtime\_dialog Go示例demo，修复录音上传慢问题|

上一篇

产品简介

下一篇

端到端Android SDK 接口文档
