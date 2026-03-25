#!/bin/bash
# 符合 AgentKernel Stdin/Stdout 协议的包装器
read -r INPUT_DATA
# 此处逻辑通常调用 Python 处理 LLM 请求
# 模拟执行逻辑：
python3 - << python_end
import json, sys
try:
    data = json.loads('$INPUT_DATA')
    # 模拟意境分析与模板填充
    res = {
        "status": "success",
        "suno_style": "Cinematic Folk, Acoustic Guitar, Ethereal, 85 BPM, Male emotive vocals",
        "suno_lyrics": "[Intro]\n" + data.get('lyrics', ''),
        "bpm_suggestion": 85
    }
    print(json.dumps(res, ensure_ascii=False))
except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}))
python_end
