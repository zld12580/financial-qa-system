import sys
import os
import csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from question_loader import QuestionLoader
from answer_generator import AnswerGenerator
import time

def main():
    print("=" * 60)
    print("分批处理 - 每批10题")
    print("=" * 60)
    
    output_file = os.path.join(os.path.dirname(__file__), 'output', 'answer.csv')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    results = []
    start_idx = 0
    
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            results = list(reader)
            start_idx = len(results)
            print(f"从第 {start_idx + 1} 题继续...")
    
    print("\n加载问题...")
    loader = QuestionLoader()
    questions = loader.load_all()
    print(f"共加载 {len(questions)} 道题目")
    
    if start_idx >= len(questions):
        print("所有题目已处理完成！")
        return
    
    generator = AnswerGenerator()
    batch_size = 10
    
    start_time = time.time()
    
    for i in range(start_idx, len(questions)):
        question = questions[i]
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
            print(f"{i+1}. {qid}: {answer} (本批耗时: {elapsed:.1f}s)")
            
            if (i + 1) % batch_size == 0:
                print(f"  保存中间结果...")
                with open(output_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['qid', 'answer', 'prompt_tokens', 'completion_tokens', 'total_tokens'])
                    writer.writeheader()
                    writer.writerows(results)
                start_time = time.time()
                
        except Exception as e:
            print(f"  错误 {qid}: {e}")
            results.append({
                'qid': qid,
                'answer': 'A',
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0
            })
    
    print("\n保存最终结果...")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['qid', 'answer', 'prompt_tokens', 'completion_tokens', 'total_tokens'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n完成！文件: {output_file}")
    
    print("\n答案分布统计：")
    answer_stats = {}
    for result in results:
        ans = result['answer']
        answer_stats[ans] = answer_stats.get(ans, 0) + 1
    
    for ans in sorted(answer_stats.keys()):
        count = answer_stats[ans]
        print(f"  {ans}: {count}次")


if __name__ == "__main__":
    main()