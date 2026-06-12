import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from question_loader import QuestionLoader
from answer_generator import AnswerGenerator
from report_generator import ReportGenerator
from tqdm import tqdm


def main():
    print("加载问题...")
    loader = QuestionLoader()
    questions = loader.load_all()
    print(f"共加载 {len(questions)} 道题目")
    
    print("\n生成答案...")
    generator = AnswerGenerator()
    results = []
    
    for question in tqdm(questions, desc="处理进度"):
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
    
    print(f"\n完成！报告已保存至: {output_file}")
    print(f"总Token消耗: 输入={total_tokens[0]}, 输出={total_tokens[1]}, 合计={total_tokens[2]}")


if __name__ == "__main__":
    main()