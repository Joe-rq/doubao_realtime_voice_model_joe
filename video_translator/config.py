import uuid

# 豆包API配置
DOUBAO_CONFIG = {
    "base_url": "wss://openspeech.bytedance.com/api/v3/realtime/dialogue",
    "headers": {
        "X-Api-App-ID": "your-app-id",  # 替换为你的APP ID
        "X-Api-Access-Key": "your-access-key",  # 替换为你的Access Key
        "X-Api-Resource-Id": "volc.speech.dialog",
        "X-Api-App-Key": "PlgvMymc7f3tQnJ6",
        "X-Api-Connect-Id": str(uuid.uuid4()),
    }
}

# 音频配置
AUDIO_CONFIG = {
    "format": "pcm",
    "channels": 1,
    "sample_rate": 16000,
    "chunk_size": 1024,
    "format_bits": 16
}

# 翻译配置
TRANSLATION_CONFIG = {
    "source_language": "en",
    "target_language": "zh",
    "enable_interim_results": True,
    "enable_punctuation": True
}