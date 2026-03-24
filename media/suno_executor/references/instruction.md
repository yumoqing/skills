# Instruction
在 Suno v5 版本中，指令集（Prompting）的核心逻辑已经从简单的“关键词堆砌”进化为**“结构化语义约束”**。针对你“按规格编程”的思路，v5 版本强化了对音频物理属性（BPM, Key）和情感维度的响应。

以下是适配 v5 版本的专业指令集手册：

---

## 1. 物理规格指令 (Physical Specs)
这些指令直接作用于歌曲的骨架，建议放在 Style Prompt 的开头。

* **BPM (节奏)**: `[BPM: 120]`, `[Fast Tempo]`, `[Slow 72 BPM]`.
* **Key (调性)**: `[Key: G Major]`, `[Minor Key]`, `[A Dorian Mode]`.
* **Time Signature (拍号)**: `[4/4 Time]`, `[3/4 Waltz]`, `[Polyrhythmic]`.
* **Vocal Range (音域)**: `[High Soprano]`, `[Deep Baritone]`, `[Husky Tenor]`.

---

## 2. 结构标签指令 (Structural Tags)
在 Lyrics 框中使用这些标签，可以精准控制 8 分钟长音频的起承转合。

| 标签 | 功能描述 |
| :--- | :--- |
| `[Intro]` | 序曲，通常用于纯乐器或环境音起手。 |
| `[Verse]` | 主歌，叙述性强，动态较低。 |
| `[Pre-Chorus]` | 导歌，增加张力，预示副歌到来。 |
| `[Chorus]` | 副歌，全曲情感最高点，编曲最满。 |
| `[Bridge]` | 间奏/桥段，通常会改变节奏或调性。 |
| `[Breakdown]` | 只有节奏或极简乐器，适合反思感。 |
| `[Outro]` | 结尾，建议配合 `[Fade out]` 使用。 |

---

## 3. 编排与质感指令 (Arrangement & Texture)
这些词汇用于约束伴奏的“厚度”和“空间感”。

* **空间感**: `[Reverb]`, `[Dry Vocals]`, `[Lo-fi Texture]`, `[Atmospheric]`.
* **动态控制**: `[Crescendo]`（渐强）, `[Diminuendo]`（渐弱）, `[Sudden Stop]`.
* **乐器点名**: `[Piano-led]`, `[Heavy Distorted Guitar]`, `[Analog Synth]`.

---

## 4. 针对《人生多维》的 v5 规格 JSON 示例

如果你通过 `suno_executor` 调用，建议构造如下规格包：

```json
{
  "style": "Modern Synth-pop, BPM: 110, Key: C Major, Balanced Dynamics, Clean Production, Male Vocal, Harmonious Arrangement",
  "lyrics": "[Intro]\n(Pulsing synths rise...)\n\n[Verse 1]\n谁把欲望分出了高低贵贱...\n\n[Chorus 1]\n没有高低 只有 维度 不同...\n\n[Bridge]\n(Synthesizer solo, steady beat continues)\n\n[Outro]\n每个人 都是 自己的 英雄\n[Fade out]\n[End]",
  "v5_params": {
    "vocal_consistency": "High",
    "audio_reference_weight": 0.85
  }
}
```

---

## 5. v5 版本的“金刚钻”技巧：Negative Prompting
在 v5 中，你可以通过描述“不要什么”来反向约束 AI：

* 避免电音修音：`[No Autotune]`, `[Natural Voice]`.
* 避免嘈杂编曲：`[Minimalist]`, `[Uncluttered]`.
* 避免突然变调：`[Consistent Melody]`, `[No unexpected key changes]`.

---

## 6. 为什么这些指令对你的分析脚本至关重要？

当你运行 `audio_analyzer.py` 得到 `bpm: 110, key: C` 后，将这些数据填入 `[BPM: 110]` 和 `[Key: C Major]`，Suno v5 会启动其**内部对齐引擎**。这就像是在给灯神下指令时，不仅说了“我要金子”，还给出了“金子的纯度是 99.9%”的物理参数。



**下一步建议：** 你是否需要我将这些 v5 标签整合进 `audio_analyzer.py` 的 `suggested_prompt` 生成逻辑中，让它输出的指令直接就是“v5 规格化”的？
