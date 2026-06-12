import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from question_loader import QuestionLoader
from answer_generator import AnswerGenerator
from report_generator import ReportGenerator
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
            
            if i % 10 == 0:
                elapsed = time.time() - start_time
                print(f"已处理 {i}/{len(questions)} 题，耗时 {elapsed:.1f}秒")
                
        except Exception as e:
            print(f"\n处理问题 {qid} 失败: {e}")
            results.append({
                'qid': qid,
                'answer': 'A',
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0
            })
    
    total_tokens = generator.get_total_tokens()
    
    print("\n生成报告...")
    reporter = ReportGenerator()
    output_file = reporter.generate(results, total_tokens)
    
    elapsed = time.time() - start_time
    print(f"\n完成！报告已保存至: {output_file}")
    print(f"总耗时: {elapsed:.1f}秒")
    print(f"总Token消耗: 输入={total_tokens[0]}, 输出={total_tokens[1]}, 合计={total_tokens[2]}")


if __name__ == "__main__":
    main()