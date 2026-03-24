---
name: whisperx_aligner
description: 使用WhisperX实现歌词与音频的毫秒级强制对齐
---

# SKILLS.md：歌词音频对齐器 (whisperx_aligner)

## 1. 技能概述
`whisperx_aligner` 接收音频文件和纯文本歌词，通过 WhisperX 的强制对齐模型（Forced Alignment），输出包含每个词/句起始时间的 JSON 结果。

## 2. 接口规范 (Stdin/Stdout)

### 输入参数 (JSON)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `audio_path` | str | 待对齐的音频本地路径 |
| `lyrics_text` | str | 原始歌词文本（建议按行分隔） |
| `device` | str | 运行设备：`cuda` (推荐) 或 `cpu` |

### 输出结果 (JSON)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `status` | str | `success` 或 `error` |
| `segments` | list | 包含 `start`, `end`, `text` 的对齐片段列表 |
| `word_segments` | list | 逐词对齐结果（可选，取决于模型支持） |

## 3. 数据库持久化适配
结果将以 JSON 字符串形式存入 `agent_runs` 表的 `state` 字段。符合 `table.md` 规范。

