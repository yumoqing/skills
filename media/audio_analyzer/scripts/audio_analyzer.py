import sys
import json
import os
import av
import numpy as np
import librosa
import traceback
import asyncio

def resample_audio_pyav(file_path, target_sr=8000):
    """
    使用 PyAV 将音频重采样为目标采样率和单声道
    返回: numpy array (float32)
    """
    container = av.open(file_path)
    # 获取第一个音频流
    stream = container.streams.audio[0]
    
    # 定义重采样器：s16格式(librosa常用float32，这里先转s16再转float), 8000Hz, 单声道
    resampler = av.AudioResampler(
        format='s16p',
        layout='mono',
        rate=target_sr,
    )

    audio_data = []
    for frame in container.decode(stream):
        # 重采样
        frame.pts = None
        resampled_frames = resampler.resample(frame)
        if resampled_frames:
            for resampled_frame in resampled_frames:
                # 转换为 numpy 数组并归一化为 float32
                array = resampled_frame.to_ndarray().reshape(-1)
                audio_data.append(array)
    
    container.close()
    
    # 拼接并转换为 float32 供 librosa 使用
    if not audio_data:
        return None
    
    full_audio = np.concatenate(audio_data).astype(np.float32) / 32768.0
    return full_audio

async def analyze_audio(file_path):
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found: {file_path}"}

    try:
        # 1. 转换：单声道 + 8000Hz (使用 PyAV)
        # 直接在内存中获取重采样后的数据，不产生临时文件
        y_8k = resample_audio_pyav(file_path, target_sr=8000)
        if y_8k is None:
            return {"status": "error", "message": "Failed to decode audio"}
        
        sr_8k = 8000
        duration = len(y_8k) / sr_8k

        # 2. 分析节奏 (BPM)
        tempo, _ = librosa.beat.beat_track(y=y_8k, sr=sr_8k)
        bpm = int(round(float(tempo)))

        # 3. 分析调性 (Key)
        # 8000Hz 下做 CQT 运算量极小
        chroma = librosa.feature.chroma_cqt(y=y_8k, sr=sr_8k)
        chroma_avg = np.mean(chroma, axis=1)
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key_idx = np.argmax(chroma_avg)
        key_detected = key_names[key_idx]

        # 4. 生成 Suno 约束指令
        prompt_constraints = (
            f"Genre: Modern Acoustic, BPM: {bpm}, Key: {key_detected}, "
            f"Fixed melody, Steady tempo, 8000Hz Analysis Reference."
        )

        return {
            "status": "success",
            "bpm": bpm,
            "key": key_detected,
            "duration_sec": round(duration, 2),
            "suggested_prompt": prompt_constraints,
            "analysis_sr": sr_8k,
            "file_path": file_path
        }

    except Exception as e:
        return {
            "status": "error", 
            "message": str(e), 
            "trace": traceback.format_exc()
        }

if __name__ == "__main__":
    # 符合 AgentKernel 的 Stdin/Stdout 协议
    async def main():
        try:
            input_raw = sys.stdin.read()
            if not input_raw:
                return
                
            params = json.loads(input_raw)
            f_path = params.get("file_path")
            
            result = await analyze_audio(f_path)
            
            # 输出 JSON 供内核持久化到 agent_runs 表的 state 字段
            sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"status": "error", "message": str(e)}) + "\n")

    asyncio.run(main())

