#!/bin/bash
# 金融问答系统 - 快速启动脚本 (Linux/Mac)

echo "===================================="
echo "金融问答系统 - 快速启动"
echo "===================================="
echo ""

# 检查Python是否安装
echo "[1/3] 检查Python..."
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查依赖是否安装
echo "[2/3] 检查依赖..."
if ! python3 -c "import openai" &> /dev/null; then
    echo "[安装] 正在安装依赖..."
    pip3 install -r qa_system/requirements.txt
fi

# 检查.env文件
echo "[3/3] 检查配置..."
if [ ! -f .env ]; then
    echo "[警告] 未找到.env文件"
    if [ -f .env.example ]; then
        echo "[提示] 正在从.env.example创建.env..."
        cp .env.example .env
        echo "[重要] 请编辑.env文件，填入你的API密钥"
        exit 0
    fi
fi

# 运行主程序
echo ""
echo "[启动] 运行主程序..."
python3 qa_system/main.py