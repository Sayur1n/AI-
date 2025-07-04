import os
import requests
from pathlib import Path
from datetime import datetime, timedelta
from .config import Config
import uuid

class UploadService:
    def __init__(self):
        self.api_key = Config.DASHSCOPE_API_KEY
        self.model_name = Config.MODEL_NAME
        
    def get_upload_policy(self):
        """获取文件上传凭证"""
        url = "https://dashscope.aliyuncs.com/api/v1/uploads"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        params = {
            "action": "getPolicy",
            "model": self.model_name
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to get upload policy: {response.text}")
        
        return response.json()['data']

    def upload_file_to_oss(self, policy_data, file_path):
        """将文件上传到临时存储OSS"""
        file_name = Path(file_path).name
        # 添加唯一标识避免文件名冲突
        unique_name = f"{uuid.uuid4().hex}_{file_name}"
        key = f"{policy_data['upload_dir']}/{unique_name}"
        
        with open(file_path, 'rb') as file:
            files = {
                'OSSAccessKeyId': (None, policy_data['oss_access_key_id']),
                'Signature': (None, policy_data['signature']),
                'policy': (None, policy_data['policy']),
                'x-oss-object-acl': (None, policy_data['x_oss_object_acl']),
                'x-oss-forbid-overwrite': (None, policy_data['x_oss_forbid_overwrite']),
                'key': (None, key),
                'success_action_status': (None, '200'),
                'file': (file_name, file)
            }
            
            response = requests.post(policy_data['upload_host'], files=files)
            if response.status_code != 200:
                raise Exception(f"Failed to upload file: {response.text}")
        
        return f"oss://{key}"

    def upload_file_and_get_url(self, file_path):
        """上传文件并获取公网URL"""
        # 1. 获取上传凭证
        policy_data = self.get_upload_policy() 
        # 2. 上传文件到OSS
        oss_url = self.upload_file_to_oss(policy_data, file_path)
        
        return oss_url 