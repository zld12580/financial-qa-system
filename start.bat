@echo off
REM 金融问答系统 - 快速启动脚本 (Windows)

echo ====================================
echo 金融问答系统 - 快速启动
echo ====================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo [1/3] 检查依赖...
pip show openai >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装依赖...
    pip install -r qa_system\requirements.txt
)

REM 检查.env文件
echo [2/3] 检查配置...
if not exist .env (
    echo [警告] 未找到.env文件
    if exist .env.example (
        echo [提示] 正在从.env.example创建.env...
        copy .env.example .env
        echo [重要] 请编辑.env文件，填入你的API密钥
        pause
        exit /b 0
    )
)

REM 运行主程序
echo [3/3] 启动程序...
echo.
python qa_system\main.py

pause