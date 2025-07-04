#!/usr/bin/env python3
"""
AI模特试衣系统启动脚本
"""

import os
import sys
import uvicorn
from pathlib import Path

# 添加backend目录到Python路径
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from backend.config import Config

def main():
    """启动应用"""
    print("🚀 启动AI模特试衣系统...")
    print(f"📍 服务器地址: http://{Config.HOST}:{Config.PORT}")
    print(f"🔑 API Key: {'已配置' if Config.DASHSCOPE_API_KEY else '未配置'}")
    
    if not Config.DASHSCOPE_API_KEY:
        print("❌ 错误: 请在.env文件中配置DASHSCOPE_API_KEY")
        sys.exit(1)
    
    # 启动服务器
    uvicorn.run(
        "backend.main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 