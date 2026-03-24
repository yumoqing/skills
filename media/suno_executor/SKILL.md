---
name: suno_executor
description: 调用Suno接口实现音乐创作
---

# suno_executor
调用suno提供的API，能够完成歌曲创作，配乐，以及改写功能

## 1. 技能概述
`suno_executor` 负责将用户的输入歌词，风格，以及歌名，参考音频（可选），自动补全音乐指令后，调用suno的API完成音乐创作

## 2. 指令集
[指令集](references/instruction.md)含有suno V5的全部指令集，补全音乐指令需要参考这个指令集

## 3. 创作歌曲
需要输入歌词，风格和歌名

### 输入参数 (JSON)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `title` |
| `lyrics` |
| `style` |


| `url` | str | 原始清唱音频的公网url |
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

