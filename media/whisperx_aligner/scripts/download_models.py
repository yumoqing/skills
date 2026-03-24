from huggingface_hub import snapshot_download
import os

def download_whisperx_deps():
    print("[*] Starting model pre-download...")
    # 1. 下载 VAD 模型 (用于语音检测)
    snapshot_download(repo_id="pyannote/segmentation-3.0", local_dir="models/vad")
    
    # 2. 下载中文对齐模型 (Wav2Vec2 7000h 中文版本)
    snapshot_download(repo_id="jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn", 
                      local_dir="models/align_zh")
    
    print("[+] Models downloaded to ./models/")

if __name__ == "__main__":
    download_whisperx_deps()
