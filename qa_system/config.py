import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(env_path)

QUESTIONS_DIR = os.path.join(BASE_DIR, "public_dataset_upload", "questions")
RAW_DIR = os.path.join(BASE_DIR, "public_dataset_upload", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "qa_system", "output")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://llmapi.inner.sincetech.com/v1")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "DeepSeek-V4-Flash")

MAX_PDF_PAGES = 35
MAX_CONTEXT_LENGTH = 25000