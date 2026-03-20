import sys
import json
import asyncio
import aiohttp
import os
import traceback

class SunoExecutor:
    def __init__(self):
        # 从环境变量或配置文件获取 API 密钥
        self.api_key = os.getenv("SUNO_API_KEY", "YOUR_API_KEY")
        self.base_url = "https://api.suno.ai/v1" # 假设的 API 地址
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def upload_audio(self, file_path):
        """上传原始清唱音频获取标识"""
        url = f"{self.base_url}/upload"
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field('file', open(file_path, 'rb'))
            async with session.post(url, data=data, headers=self.headers) as resp:
                res = await resp.json()
                return res.get("audio_id")

    async def generate_with_constraints(self, audio_id, specs):
        """发送带规格约束的生成指令"""
        url = f"{self.base_url}/generate"
        payload = {
            "vocal_id": audio_id,
            "gpt_description_prompt": f"{specs['prompt']}. BPM: {specs['bpm']}, Key: {specs['key']}",
            "make_instrumental": True, # 重点：生成伴奏模式
            "wait_audio": False 
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=self.headers) as resp:
                return await resp.json()

    async def poll_result(self, task_id, timeout=600):
        """轮询任务状态直至完成"""
        url = f"{self.base_url}/task/{task_id}"
        start_time = asyncio.get_event_loop().time()
        
        async with aiohttp.ClientSession() as session:
            while (asyncio.get_event_loop().time() - start_time) < timeout:
                async with session.get(url, headers=self.headers) as resp:
                    res = await resp.json()
                    if res.get("status") == "completed":
                        return res.get("audio_url")
                    elif res.get("status") == "failed":
                        raise Exception("Suno task failed")
                
                await asyncio.sleep(10) # 每10秒轮询一次
        raise TimeoutError("Suno generation timeout")

async def main():
    try:
        # 1. 接收内核传递的规格参数
        input_raw = sys.stdin.read()
        if not input_raw: return
        params = json.loads(input_raw)
        
        executor = SunoExecutor()
        
        # 2. 执行流程
        # A. 上传
        audio_id = await executor.upload_audio(params['file_path'])
        
        # B. 提交带约束的任务
        task_info = await executor.generate_with_constraints(audio_id, params)
        task_id = task_info.get("id")
        
        # C. 轮询等待结果
        final_url = await executor.poll_result(task_id)
        
        # 3. 返回结果给内核回填数据库
        result = {
            "status": "success",
            "audio_url": final_url,
            "suno_id": task_id,
            "specs_applied": {"bpm": params['bpm'], "key": params['key']}
        }
        sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
        
    except Exception as e:
        sys.stdout.write(json.dumps({
            "status": "error", 
            "message": str(e),
            "trace": traceback.format_exc()
        }) + "\n")

if __name__ == "__main__":
    asyncio.run(main())

