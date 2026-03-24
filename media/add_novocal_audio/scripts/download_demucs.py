import demucs.api
import os

def preload_demucs():
    print("[*] Preloading Demucs model: htdemucs...")
    # 实例化 API 会自动触发模型下载并缓存到 ~/.cache/torch/hub/
    separator = demucs.api.Separator(model="htdemucs", device="cpu") 
    print("[+] Model htdemucs preloaded successfully.")

if __name__ == "__main__":
    preload_demucs()
