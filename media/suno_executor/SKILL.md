---
name: suno_executor
description: 调用Suno接口上传音频并根据规格约束生成伴奏
---

# SKILLS.md：Suno伴奏生成执行器 (suno_executor)

## 1. 技能概述
`suno_executor` 负责将用户的原始清唱音频上传至音乐生成引擎，并应用 `audio_analyzer` 输出的节奏与调性约束，完成高保真的伴奏合成。

## 2. 接口规范 (Stdin/Stdout)

### 输入参数 (JSON)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `file_path` | str | 原始清唱音频的本地路径 |
| `bpm` | int | 节奏规格 (来自分析节点) |
| `key` | str | 调性规格 (来自分析节点) |
| `prompt` | str | 风格描述词 (可由分析节点生成或用户提供) |
| `lyrics` | str | 歌词内容，用于对齐音频结构 |

### 输出结果 (JSON)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `status` | str | `success` 或 `error` |
| `audio_url` | str | 生成的带伴奏音频的远程 URL |
| `suno_id` | str | Suno 侧的任务唯一标识 |

