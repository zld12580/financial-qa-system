"""
配置管理

加载环境变量并提供全局配置。
"""

import os
from dotenv import load_dotenv

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    print(f"警告: 未找到.env文件，请从.env.example创建并配置")

# 目录配置
QUESTIONS_DIR = os.path.join(BASE_DIR, "public_dataset_upload", "questions")
RAW_DIR = os.path.join(BASE_DIR, "public_dataset_upload", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "qa_system", "output")

# API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://llmapi.inner.sincetech.com/v1")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "DeepSeek-V4-Flash")

# 验证API配置
if not DEEPSEEK_API_KEY:
    print("=" * 60)
    print("警告: DEEPSEEK_API_KEY未配置！")
    print("请在.env文件中设置DEEPSEEK_API_KEY")
    print("系统将以mock模式运行，返回默认答案")
    print("=" * 60)

# 文档提取配置
MAX_PDF_PAGES = 35  # PDF最大读取页数
MAX_CONTEXT_LENGTH = 25000  # 最大上下文长度（字符）

# 输出配置
OUTPUT_ENCODING = 'utf-8'  # 输出文件编码
CSV_DELIMITER = ','  # CSV分隔符

def print_config():
    """打印当前配置信息"""
    print("=" * 60)
    print("当前配置:")
    print(f"  项目根目录: {BASE_DIR}")
    print(f"  问题目录: {QUESTIONS_DIR}")
    print(f"  文档目录: {RAW_DIR}")
    print(f"  输出目录: {OUTPUT_DIR}")
    print(f"  API地址: {DEEPSEEK_API_URL}")
    print(f"  模型: {DEEPSEEK_MODEL}")
    print(f"  API密钥: {'已配置' if DEEPSEEK_API_KEY else '未配置'}")
    print(f"  PDF最大页数: {MAX_PDF_PAGES}")
    print(f"  最大上下文长度: {MAX_CONTEXT_LENGTH}")
    print("=" * 60)

if __name__ == "__main__":
    print_config()
