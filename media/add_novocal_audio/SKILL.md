---
name: add_novocal_audio
description: 拆解输入视频文件，得到无声视频，伴奏，原音频三个文件，最后按照KTV规格要求合并无声视频+伴奏+原音频，得到KTV视频文件，遵守KTV音乐视频的规范
---

# add_novocal_audio

## 1. 技能概述
scripts/ktv.sh脚本将输入视频，拆解成无声视频，伴奏，原音频，按照KTV
规格要求合并无声视频+伴奏+原音频，输出合成的KTV视频文件

## 2. 初始化与部署 (Setup & Initialization)
需要用到meta的demucs模块，并要用到相关的大模型，第一次使用会自动下载所需模型，
对于没有外网能力的环境，可以在第一次执行时记录下下载网址，找个外网环境下载后
传过来

### 2.1 依赖环境安装
```bash
# 安装 Python 依赖
python3 -m venv py3
py3/bin/pip install demucs torch torchvision torchaudio
py3/bin/python scripts/download_demucs.py
```

## 3. 接口规范 (Stdin/Stdout)

### 3.1 输入参数 (JSON)
内核通过 Stdin 传入：
| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `file_path` | str | 是 | 原视频文件 |

### 3.2 输出结果 (JSON)
通过 Stdout 返回：
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `status` | str | `success` 或 `error` |
| `ktv_file` | str | 最后合成的ktv视频文件 |

## 4. 运行逻辑与语法说明

### 4.1 调用命令语法
```bash
bash scripts/ktv.sh
```
## 5. 附加参考资料
* **模型对比**：`htdemucs_ft` 效果最好但速度较慢；`htdemucs` 平衡性最佳。
* **硬件建议**：对于 8 分钟音频，H100 处理时间约为 **30-50秒**；CPU 可能需要 **5-10分钟**。
* **官方文档**：[facebookresearch/demucs](https://github.com/facebookresearch/demucs)

