#!/usr/bin/env python3
"""
AI模特试衣系统测试脚本
"""

import os
import sys
from pathlib import Path

def test_environment():
    """测试环境配置"""
    print("🔍 测试环境配置...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python版本过低，需要Python 3.8或更高版本")
        return False
    print(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查.env文件
    if not os.path.exists(".env"):
        print("❌ 未找到.env文件，请先配置环境变量")
        return False
    print("✅ 找到.env文件")
    
    # 检查API Key配置
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❌ 请在.env文件中配置有效的DASHSCOPE_API_KEY")
        return False
    print("✅ API Key已配置")
    
    return True

def test_dependencies():
    """测试依赖包"""
    print("\n🔍 测试依赖包...")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "requests",
        "python-dotenv",
        "sqlalchemy",
        "pillow"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True

def test_backend_modules():
    """测试后端模块"""
    print("\n🔍 测试后端模块...")
    
    try:
        from backend.config import Config
        print("✅ 配置模块")
        
        from backend.database import get_db, init_db
        print("✅ 数据库模块")
        
        from backend.models import Task
        print("✅ 数据模型")
        
        from backend.upload_service import UploadService
        print("✅ 上传服务")
        
        from backend.ai_service import AIService
        print("✅ AI服务")
        
        return True
    except Exception as e:
        print(f"❌ 后端模块测试失败: {e}")
        return False

def test_file_structure():
    """测试文件结构"""
    print("\n🔍 测试文件结构...")
    
    required_files = [
        "backend/__init__.py",
        "backend/config.py",
        "backend/database.py", 
        "backend/models.py",
        "backend/upload_service.py",
        "backend/ai_service.py",
        "backend/main.py",
        "frontend/index.html",
        "requirements.txt",
        "env.example",
        "run.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ 缺少文件: {', '.join(missing_files)}")
        return False
    
    return True

def main():
    """主测试函数"""
    print("🚀 AI模特试衣系统测试")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_environment,
        test_dependencies,
        test_backend_modules
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！系统可以正常启动")
        print("\n启动命令:")
        print("python run.py")
    else:
        print("❌ 测试失败，请检查上述问题")
    
    return all_passed

if __name__ == "__main__":
    main() 