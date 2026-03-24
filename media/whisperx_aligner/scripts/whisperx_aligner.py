#!/d/ymq/py3/bin/python
import sys
import json
import os
import whisperx
import torch
import traceback
import asyncio

async def align_lyrics(audio_path, lyrics_text, device="cuda"):
	"""
	使用 WhisperX 进行强制对齐
	"""
	try:
		# 1. 准备数据
		# WhisperX 需要加载模型，生产环境下建议将 model 实例对象池化
		compute_type = "float16" if device == "cuda" else "int8"
		
		# 2. 加载模型 (仅加载对齐所需的 model)
		# 注意：这里我们直接使用 align 模型，假设已知语言为中文 'zh'
		model_a, metadata = whisperx.load_align_model(
			language_code="zh", 
			device=device, 
			compute_type=compute_type
		)

		# 3. 加载音频
		audio = whisperx.load_audio(audio_path)

		# 4. 封装成 WhisperX 格式的 segments
		# 假设输入的 lyrics_text 是按行分隔的
		lines = [line.strip() for line in lyrics_text.split('\n') if line.strip()]
		raw_segments = [{"text": line} for line in lines]

		# 5. 执行对齐
		result = whisperx.align(
			raw_segments, 
			model_a, 
			metadata, 
			audio, 
			device, 
			return_char_alignments=False
		)

		# 释放显存 (生产环境重要点)
		del model_a
		if device == "cuda":
			torch.cuda.empty_cache()

		return {
			"status": "success",
			"segments": result["segments"],
			"word_segments": result.get("word_segments", [])
		}

	except Exception as e:
		return {
			"status": "error",
			"message": str(e),
			"trace": traceback.format_exc()
		}

async def main():
	# 符合 AgentKernel 的 Stdin/Stdout 协议
	input_raw = sys.stdin.read()
	if not input_raw:
		return
		
	try:
		params = json.loads(input_raw)
		audio_path = params.get("audio_path")
		lyrics_text = params.get("lyrics_text")
		device = params.get("device", "cuda" if torch.cuda.is_available() else "cpu")
		
		# 执行对齐
		result = await align_lyrics(audio_path, lyrics_text, device)
		
		# 输出 JSON
		sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
		sys.stdout.flush()
	except Exception as e:
		sys.stdout.write(json.dumps({"status": "error", "message": str(e)}) + "\n")

if __name__ == "__main__":
	asyncio.run(main())
