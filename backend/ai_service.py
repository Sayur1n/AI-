import requests
import time
from .config import Config

class AIService:
    def __init__(self):
        self.api_key = Config.DASHSCOPE_API_KEY
        self.model_name = Config.MODEL_NAME
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"
        
    def submit_task(self, person_image_url, top_garment_url=None, bottom_garment_url=None):
        """提交AI试衣任务"""
        url = f"{self.base_url}/services/aigc/image2image/image-synthesis"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"
        }
        
        # 构建请求数据
        data = {
            "model": self.model_name,
            "input": {
                "person_image_url": person_image_url
            },
            "parameters": {
                "resolution": -1,
                "restore_face": True
            }
        }
        
        # 添加上装或下装（至少一个）
        if top_garment_url:
            data["input"]["top_garment_url"] = top_garment_url
        if bottom_garment_url:
            data["input"]["bottom_garment_url"] = bottom_garment_url
            
        # 验证至少有一个服装图片
        if not top_garment_url and not bottom_garment_url:
            raise ValueError("至少需要提供上装或下装图片中的一个")
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code != 200:
            raise Exception(f"Failed to submit task: {response.text}")
        
        result = response.json()
        return result["output"]["task_id"]
    
    def get_task_status(self, task_id):
        """获取任务状态和结果"""
        url = f"{self.base_url}/tasks/{task_id}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to get task status: {response.text}")
        
        return response.json()
    
    def wait_for_completion(self, task_id, max_wait_time=300, check_interval=5):
        """等待任务完成"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            result = self.get_task_status(task_id)
            status = result["output"]["task_status"]
            
            if status == "SUCCEEDED":
                return result
            elif status == "FAILED":
                raise Exception(f"Task failed: {result.get('output', {}).get('message', 'Unknown error')}")
            elif status in ["PENDING", "PRE-PROCESSING", "RUNNING", "POST-PROCESSING"]:
                time.sleep(check_interval)
            else:
                raise Exception(f"Unknown task status: {status}")
        
        raise Exception("Task timeout") 