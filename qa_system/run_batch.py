import sys
import os
import csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from question_loader import QuestionLoader
from answer_generator import AnswerGenerator
import time

def main():
    print("加载问题...")
    loader = QuestionLoader()
    questions = loader.load_all()
    print(f"共加载 {len(questions)} 道题目")
    
    print("\n生成答案...")
    generator = AnswerGenerator()
    results = []
    
    start_time = time.time()
    
    for i, question in enumerate(questions, 1):
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
            
            if i % 5 == 0:
                elapsed = time.time() - start_time
                avg_time = elapsed / i
                remaining = (len(questions) - i) * avg_time
                print(f"进度: {i}/{len(questions)} | 已耗时: {elapsed:.1f}s | 预计剩余: {remaining:.1f}s")
                
        except Exception as e:
            print(f"错误 {qid}: {e}")
            results.append({
                'qid': qid,
                'answer': 'A',
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0
            })
    
    total_tokens = generator.get_total_tokens()
    
    print("\n保存结果...")
    output_file = os.path.join(os.path.dirname(__file__), 'output', 'answer.csv')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['qid', 'answer', 'prompt_tokens', 'completion_tokens', 'total_tokens'])
        writer.writeheader()
        writer.writerows(results)
    
    elapsed = time.time() - start_time
    print(f"\n完成！文件: {output_file}")
    print(f"总耗时: {elapsed:.1f}秒")
    print(f"Token消耗: 输入={total_tokens[0]}, 输出={total_tokens[1]}, 合计={total_tokens[2]}")


if __name__ == "__main__":
    main()