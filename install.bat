@echo off
echo 安装AI模特试衣系统...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装

REM 创建虚拟环境
echo 创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo 错误: 创建虚拟环境失败
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级pip
echo 升级pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 安装Python依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 安装依赖失败
    pause
    exit /b 1
)

REM 创建.env文件
if not exist ".env" (
    echo 创建.env文件...
    copy "env.example" ".env"
    echo.
    echo ⚠️  请编辑.env文件，配置您的阿里云百炼API Key
    echo.
)

echo.
echo 🎉 安装完成！
echo.
echo 下一步:
echo 1. 编辑.env文件，配置您的API Key
echo 2. 运行 start.bat 启动系统
echo.
pause 