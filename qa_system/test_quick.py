import sys
import os
import csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from question_loader import QuestionLoader
from answer_generator import AnswerGenerator
import time

def main():
    print("=" * 60)
    print("优化后的QA系统测试 (前10题)")
    print("=" * 60)
    
    print("\n加载问题...")
    loader = QuestionLoader()
    questions = loader.load_all()
    print(f"共加载 {len(questions)} 道题目")
    
    print("\n生成答案...")
    generator = AnswerGenerator()
    results = []
    
    start_time = time.time()
    
    for i, question in enumerate(questions[:10], 1):
        qid = question.get('qid', '')
        
        try:
            answer, prompt_tokens, completion_tokens = generator.generate(question)
            
            results.append({
                'qid': qid,
                'answer': answer,
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens
            })
            
            elapsed = time.time() - start_time
            print(f"{i}. {qid}: {answer} (耗时: {elapsed:.1f}s)")
                
        except Exception as e:
            print(f"错误 {qid}: {e}")
            results.append({
                'qid': qid,
                'answer': 'A',
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0
            })
    
    elapsed = time.time() - start_time
    print(f"\n测试完成！总耗时: {elapsed:.1f}秒")
    
    print("\n答案分布：")
    answer_stats = {}
    for result in results:
        ans = result['answer']
        answer_stats[ans] = answer_stats.get(ans, 0) + 1
    
    for ans in sorted(answer_stats.keys()):
        count = answer_stats[ans]
        print(f"  {ans}: {count}次")


if __name__ == "__main__":
    main()