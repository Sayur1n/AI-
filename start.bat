@echo off
echo 启动AI模特试衣系统...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 检查.env文件是否存在
if not exist ".env" (
    echo 警告: 未找到.env文件，正在复制示例文件...
    copy "env.example" ".env"
    echo 请编辑.env文件，配置您的API Key
    pause
)

REM 检查虚拟环境是否存在
if exist "venv\Scripts\activate.bat" (
    echo 激活虚拟环境...
    call venv\Scripts\activate.bat
) else (
    echo 未找到虚拟环境，使用系统Python
    echo 建议运行 install.bat 创建虚拟环境
)

REM 安装依赖
echo 安装Python依赖...
pip install -r requirements.txt

REM 启动应用
echo 启动应用...
python run.py

pause 