---
name: whisperx_aligner
description: 使用WhisperX实现歌词与音频的毫秒级强制对齐
---
# whisperx_aligner
歌词音频对齐器 (whisperx_aligner)

## 1. 技能概述
`whisperx_aligner` 是基于 WhisperX 框架的强制对齐工具。它通过音素级分析（Forced Alignment），将纯文本歌词与音频流进行毫秒级匹配。该技能是构建 KTV 自动化生产流水线、AI 翻唱对齐的核心插件。

## 2. 初始化与部署 (Setup & Initialization)

### 2.1 依赖环境安装
```bash
# 基础依赖：需安装 ffmpeg 5.0+
apt update && apt install ffmpeg -y

# Python 库依赖
python3 -m venv py3
py3/bin/pip install whisperx
py3/bin/pip install huggingface_hub  # 用于模型预下载
```

### 2.2 模型预下载脚本 (scripts/download_models.py)
在生产环境冷启动前，执行此脚本以缓存 VAD 和对齐模型：

```bash
if [ ! -d models ]; then
	mkdir models
	py3/bin/python scripts/download_models.py
fi
```

## 3. 接口规范 (Stdin/Stdout)

### 3.1 输入参数 (JSON)
内核通过 Stdin 传入：
| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `audio_path` | str | 是 | 原始音频本地路径 |
| `lyrics_text` | str | 是 | 纯文本歌词（\n分隔） |
| `device` | str | 否 | 运行设备：`cuda` (默认) 或 `cpu` |
| `language` | str | 否 | 语言代码：`zh` (默认), `en` |

### 3.2 输出结果 (JSON)
通过 Stdout 返回：
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `status` | str | `success` 或 `error` |
| `segments` | list | 包含 `start`, `end`, `text` 的时间戳列表 |
| `word_segments` | list | 逐词对齐结果（用于 KTV 逐字变色特效） |

### 调用命令
```
py3/bin/python scripts/whisperx_aligner.py
```

## 4. 业务逻辑约束 (Runtime Constraints)

### 4.1 硬件规格
* **显存占用**：运行时约占用 **4.2GB VRAM**。
* **并发控制**：在 H100 80GB 上，建议设置 `max_concurrency: 12`。

### 4.2 数据持久化策略
对齐结果必须存入 `agent_runs` 的 `state` 字段。
* **格式要求**：JSON 压缩存储，保留 3 位小数。
* **更新逻辑**：`updated_at` 需精确到 `.999` 毫秒。

## 5. 错误代码协议
| 代码 | 含义 | 处理建议 |
| :--- | :--- | :--- |
| `ERR_CUDA_OOM` | 显存溢出 | 释放其他进程显存或进入 CPU 模式 |
| `ERR_ALIGN_FAIL` | 强制对齐失败 | 检查歌词与音频内容是否匹配（如伴奏过长） |

---

## 💡 生产实践建议：

1.  **路径规格**：在你的 `scripts/audio_analyzer.py` 中提取完规格后，紧接着调用此技能。建议将模型路径（`local_dir`）硬编码或通过 `ServerEnv` 传入，避免运行时实时从网络下载。
2.  **长音频分片**：如果音频超过 10 分钟，建议先调用 `vad` 技能切片，再并行对齐，最后合并 JSON 结果。
3.  **对齐质量监控**：如果 `segments` 中的 `start` 和 `end` 时间重叠严重，说明对齐质量差，内核应触发“人工介入”或“模型降级”标志。

**既然“对齐金刚钻”的规格书已经写全，需要我为你把这个下载脚本整合进之前那个 `setup_all_skills.sh` 中，实现真正的“全自动按规格部署”吗？**
