---
name: lyrics-evaluator
description: Evaluate lyrics quality across multiple dimensions and return structured scoring and suggestions
version: 2.0
entry: scripts/run.sh
inputs:
  - name: lyrics
    type: string
    description: The lyrics text to evaluate
outputs:
  - name: task
    type: json
    description: Task definition for LLM execution
---

# lyrics-evaluator

---

## 功能说明

该 Skill 用于对歌词进行质量评估，输出标准化任务（task），由 Skill Engine 调用 LLM 执行。

### 能力范围

- 歌词节奏分析（句长稳定性）
- 押韵分析（尾字重复率）
- 基础结构识别
- 构造标准化评估任务（prompt + schema）

### 不包含

- 不直接调用 LLM
- 不做相似度计算

---

## 输入说明

```json
{
  "lyrics": "歌词文本"
}
```

---

## 输出说明

输出一个 task JSON，由 engine 执行：

```json
{
  "prompt": "...",
  "model": "gpt-4o",
  "temperature": 0.3,
  "output_schema": {...}
}
```
