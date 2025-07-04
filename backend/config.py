import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # API配置
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
    
    # 服务器配置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_model.db")
    
    # 文件上传配置
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    # 5MB
    print(os.getenv("MAX_FILE_SIZE", 5242880))
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 5242880))  
    
    # 模型配置
    MODEL_NAME = "aitryon-plus"
    
    # 文件类型限制
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.heic'}
    
    # 图片尺寸限制
    MIN_IMAGE_SIZE = 150
    MAX_IMAGE_SIZE = 4096 