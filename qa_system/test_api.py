import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deepseek_client import DeepSeekClient

client = DeepSeekClient()

test_prompt = """
问题：以下哪个选项是正确的？

选项：
A. 选项A的内容
B. 选项B的内容
C. 选项C的内容
D. 选项D的内容

请从A、B、C、D中选择一个正确答案，只输出一个字母。
"""

answer, prompt_tokens, completion_tokens = client.call(test_prompt)

print(f"答案: {answer}")
print(f"输入Token: {prompt_tokens}")
print(f"输出Token: {completion_tokens}")