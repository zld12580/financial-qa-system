"""
示例脚本：展示如何使用金融问答系统

这个脚本演示了系统的基本使用方法。
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'qa_system'))

from question_loader import QuestionLoader
from answer_generator import AnswerGenerator

def example_single_question():
    """示例：处理单个问题"""
    print("=" * 60)
    print("示例1：处理单个问题")
    print("=" * 60)
    
    loader = QuestionLoader()
    questions = loader.load_all()
    
    if questions:
        question = questions[0]
        print(f"\n问题ID: {question['qid']}")
        print(f"问题: {question['question']}")
        print(f"选项: {question['options']}")
        
        generator = AnswerGenerator()
        answer, prompt_tokens, completion_tokens = generator.generate(question)
        
        print(f"\n答案: {answer}")
        print(f"Token消耗: {prompt_tokens + completion_tokens}")

def example_batch_processing():
    """示例：批量处理问题"""
    print("\n" + "=" * 60)
    print("示例2：批量处理前5个问题")
    print("=" * 60)
    
    loader = QuestionLoader()
    questions = loader.load_all()
    
    generator = AnswerGenerator()
    
    for i, question in enumerate(questions[:5], 1):
        qid = question.get('qid', '')
        answer, _, _ = generator.generate(question)
        print(f"{i}. {qid}: {answer}")

def example_document_extraction():
    """示例：文档提取"""
    print("\n" + "=" * 60)
    print("示例3：文档提取")
    print("=" * 60)
    
    from pdf_extractor import PDFExtractor
    
    extractor = PDFExtractor()
    
    test_docs = [
        ('financial_contracts', 'text01'),
        ('financial_reports', 'annual_byd_2024_report'),
        ('regulatory', 'csrc_0001'),
    ]
    
    for domain, doc_id in test_docs:
        text = extractor.extract_text(domain, doc_id)
        print(f"\n{domain}/{doc_id}:")
        print(f"  长度: {len(text)} 字符")
        if text:
            print(f"  前50字符: {text[:50]}...")

if __name__ == "__main__":
    print("\n金融问答系统使用示例\n")
    
    try:
        example_single_question()
        example_batch_processing()
        example_document_extraction()
        
        print("\n" + "=" * 60)
        print("示例运行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误: {e}")
        print("\n请确保：")
        print("1. 已安装所有依赖: pip install -r qa_system/requirements.txt")
        print("2. 已配置.env文件")
        print("3. 数据文件存在")