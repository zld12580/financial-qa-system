import sys
import os
import csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from question_loader import QuestionLoader
from answer_generator import AnswerGenerator
import time

def main():
    print("=" * 60)
    print("分批处理QA系统")
    print("=" * 60)
    
    print("\n加载问题...")
    loader = QuestionLoader()
    questions = loader.load_all()
    print(f"共加载 {len(questions)} 道题目")
    
    output_file = os.path.join(os.path.dirname(__file__), 'output', 'answer.csv')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    results = []
    generator = AnswerGenerator()
    
    batch_size = 20
    total_batches = (len(questions) + batch_size - 1) // batch_size
    
    start_time = time.time()
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(questions))
        batch_questions = questions[start_idx:end_idx]
        
        print(f"\n处理批次 {batch_num + 1}/{total_batches} (题目 {start_idx + 1}-{end_idx})...")
        
        for i, question in enumerate(batch_questions, 1):
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
                
                print(f"  {qid}: {answer}")
                    
            except Exception as e:
                print(f"  错误 {qid}: {e}")
                results.append({
                    'qid': qid,
                    'answer': 'A',
                    'prompt_tokens': 0,
                    'completion_tokens': 0,
                    'total_tokens': 0
                })
        
        if batch_num < total_batches - 1:
            print("  保存中间结果...")
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['qid', 'answer', 'prompt_tokens', 'completion_tokens', 'total_tokens'])
                writer.writeheader()
                writer.writerows(results)
    
    total_tokens = generator.get_total_tokens()
    
    print("\n保存最终结果...")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['qid', 'answer', 'prompt_tokens', 'completion_tokens', 'total_tokens'])
        writer.writeheader()
        writer.writerows(results)
    
    elapsed = time.time() - start_time
    print(f"\n完成！文件: {output_file}")
    print(f"总耗时: {elapsed:.1f}秒")
    print(f"Token消耗: 输入={total_tokens[0]}, 输出={total_tokens[1]}, 合计={total_tokens[2]}")
    
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