# lyrics_to_suno
歌词转Suno指令 (lyrics_to_suno)

## 1. 技能概述
`lyrics_to_suno` 负责解析用户输入的歌词意境，自动补全符合 Suno V5 规范的 Style Prompt。它能将“忧伤、深沉”转化为具体的“Minor key, Cello, 70 BPM, Melancholic”等规格参数。

## 2. 接口规范
### 输入 (JSON)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `lyrics` | str | 原始歌词全文 |
| `preferred_genre` | str | (可选) 用户偏好的大致流派 |

### 输出 (JSON)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `status` | str | `success` / `error` |
| `suno_style` | str | 最终生成的 Style 描述词 |
| `suno_lyrics` | str | 带结构标记 ([Verse], [Chorus]) 的优化歌词 |
| `bpm_suggestion` | int | 建议的 BPM 数值 |
