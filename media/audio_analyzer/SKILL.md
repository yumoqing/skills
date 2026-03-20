---
name: audio_analyzer
description: 歌曲节奏和调分析技能，提取BPM、Key等规格以约束AI生成
---

# SKILLS.md：歌曲节奏和调分析 (audio_analyzer)

## 1. 技能概述
`audio_analyzer` 是一个高性能的音频特征提取工具，专门用于分析长达 8 分钟的清唱音频。它通过数字信号处理技术提取音频的物理规格（BPM、Key、能量分布），为后续 AI 音乐生成（如 Suno）提供精确的“约束规格书”。

## 2. 接口规范 (Stdin/Stdout)

### 输入参数 (JSON)
内核通过 Stdin 传入以下结构：
| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `file_path` | str | 是 | 待分析的音频文件本地路径（支持 mp3, wav, m4a） |

### 输出结果 (JSON)
技能执行完成后通过 Stdout 返回：
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `status` | str | 状态标识：`success` 或 `error` |
| `bpm` | int | 提取的每分钟节拍数 (Beats Per Minute) |
| `key` | str | 检测到的调性（如 C, G#, Am 等） |
| `duration_sec` | float | 音频总时长（秒） |
| `suggested_prompt` | str | 自动生成的 Suno 约束指令字符串 |
| `message` | str | 错误信息（仅在 status 为 error 时出现） |

## 3. 调用方法
```
python scripts/audio_analyzer.py
```

## 4. 依赖
```
pip install PyAV librosa numpy aiofiles
```

