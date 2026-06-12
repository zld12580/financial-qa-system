import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from question_loader import QuestionLoader
from answer_generator import AnswerGenerator

print("加载问题...")
loader = QuestionLoader()
questions = loader.load_all()

print(f"共加载 {len(questions)} 道题目")

print("\n测试前5道题目...")
generator = AnswerGenerator()

for i, question in enumerate(questions[:5], 1):
    qid = question.get('qid', '')
    print(f"\n{i}. 处理问题: {qid}")
    
    try:
        answer, prompt_tokens, completion_tokens = generator.generate(question)
        print(f"   答案: {answer}")
        print(f"   Tokens: 输入={prompt_tokens}, 输出={completion_tokens}")
    except Exception as e:
        print(f"   失败: {e}")

print("\n测试完成！")