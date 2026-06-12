from typing import Dict, Tuple
from pdf_extractor import PDFExtractor
from deepseek_client import DeepSeekClient


class AnswerGenerator:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.llm_client = DeepSeekClient()
    
    def generate(self, question: Dict) -> Tuple[str, int, int]:
        qid = question.get('qid', '')
        domain = question.get('domain', '')
        question_text = question.get('question', '')
        options = question.get('options', {})
        answer_format = question.get('answer_format', 'mcq')
        doc_ids = question.get('doc_ids', [])
        
        context = ""
        if doc_ids:
            context = self.pdf_extractor.extract_multiple(domain, doc_ids)
        
        prompt = self._build_prompt(question_text, options, answer_format, context)
        
        answer, prompt_tokens, completion_tokens = self.llm_client.call(prompt)
        
        answer = self._validate_answer(answer, answer_format, options)
        
        return answer, prompt_tokens, completion_tokens
    
    def _build_prompt(self, question: str, options: Dict, answer_format: str, context: str) -> str:
        prompt_parts = []
        
        if context:
            prompt_parts.append(f"参考资料：\n{context}\n")
            prompt_parts.append("=" * 50)
            prompt_parts.append("【重要】必须严格基于上述参考资料回答，不得使用外部知识或主观推断。\n")
        
        prompt_parts.append(f"问题：{question}\n")
        
        if options:
            prompt_parts.append("选项：")
            for key in sorted(options.keys()):
                prompt_parts.append(f"{key}. {options[key]}")
            prompt_parts.append("")
        
        if answer_format == 'mcq':
            prompt_parts.append("【任务】单选题 - 选择唯一正确答案")
            prompt_parts.append("\n【分析方法】")
            prompt_parts.append("步骤1：仔细阅读问题，理解考查的核心要点")
            prompt_parts.append("步骤2：对每个选项逐一验证：")
            prompt_parts.append("  - 在参考资料中查找该选项对应的具体内容")
            prompt_parts.append("  - 判断该内容是否与选项描述完全一致")
            prompt_parts.append("  - 标记为'符合'或'不符合'")
            prompt_parts.append("步骤3：排除所有不符合的选项")
            prompt_parts.append("步骤4：确认唯一符合的选项作为答案")
            prompt_parts.append("\n【重要提示】")
            prompt_parts.append("1. 必须在资料中找到明确的文字依据")
            prompt_parts.append("2. 不能根据常识或推断选择")
            prompt_parts.append("3. 如果多个选项看似合理，选择资料中明确提到的")
            prompt_parts.append("\n【示例】")
            prompt_parts.append("问题：发行人名称是什么？")
            prompt_parts.append("选项：A.张三公司 B.李四公司 C.王五公司 D.赵六公司")
            prompt_parts.append("分析：查阅资料第X页，发行人明确写为'李四公司'，故A/C/D不符合，B符合")
            prompt_parts.append("答案：B")
            prompt_parts.append("\n请严格按照上述格式回答：")
            prompt_parts.append("分析：[逐项验证过程]")
            prompt_parts.append("答案：[单个字母]")
        elif answer_format == 'tf':
            prompt_parts.append("【任务】判断题 - 判断陈述是否正确")
            prompt_parts.append("\n【分析方法】")
            prompt_parts.append("步骤1：提取陈述中的关键信息和数据")
            prompt_parts.append("步骤2：在参考资料中定位相关内容")
            prompt_parts.append("步骤3：逐项对比陈述与资料")
            prompt_parts.append("  - 完全一致 → 正确(A)")
            prompt_parts.append("  - 存在差异 → 错误(B)")
            prompt_parts.append("步骤4：做出明确判断")
            prompt_parts.append("\n【示例】")
            prompt_parts.append("陈述：发行金额为10亿元")
            prompt_parts.append("分析：查阅资料第Y页，发行金额明确写为'15亿元'，与陈述不符")
            prompt_parts.append("答案：B")
            prompt_parts.append("\n请严格按照上述格式回答：")
            prompt_parts.append("分析：[对比过程]")
            prompt_parts.append("答案：[A=正确，B=错误]")
        elif answer_format == 'multi':
            prompt_parts.append("【任务】多选题 - 选择所有正确答案")
            prompt_parts.append("\n【分析方法】")
            prompt_parts.append("步骤1：理解问题的考查范围")
            prompt_parts.append("步骤2：对每个选项独立验证：")
            prompt_parts.append("  - 在资料中查找明确依据")
            prompt_parts.append("  - 有明确依据 → 选中")
            prompt_parts.append("  - 无明确依据或与资料不符 → 不选")
            prompt_parts.append("步骤3：汇总所有有依据的选项")
            prompt_parts.append("步骤4：注意：宁缺毋滥，不确定的选项不要选")
            prompt_parts.append("\n【示例】")
            prompt_parts.append("问题：以下哪些描述正确？")
            prompt_parts.append("选项：A.金额10亿 B.评级AAA C.期限5年 D.利率4%")
            prompt_parts.append("分析：")
            prompt_parts.append("  A: 资料显示金额15亿，不符合")
            prompt_parts.append("  B: 资料显示评级AA+，不符合")
            prompt_parts.append("  C: 资料显示期限5年，符合")
            prompt_parts.append("  D: 资料显示利率4%，符合")
            prompt_parts.append("答案：CD")
            prompt_parts.append("\n请严格按照上述格式回答：")
            prompt_parts.append("分析：[逐项验证]")
            prompt_parts.append("答案：[按字母顺序，如ABC]")
        
        return "\n".join(prompt_parts)
    
    def _validate_answer(self, answer: str, answer_format: str, options: Dict) -> str:
        answer = answer.upper().strip()
        
        valid_chars = set("ABCD")
        answer = ''.join(c for c in answer if c in valid_chars)
        
        if answer_format == 'multi':
            answer = ''.join(sorted(set(answer)))
            if not answer:
                answer = 'A'
            elif len(answer) == 4:
                answer = answer[:2]
        elif answer_format in ['mcq', 'tf']:
            if answer:
                answer = answer[0]
            else:
                answer = 'A'
        
        if answer_format == 'tf' and answer not in ['A', 'B']:
            answer = 'A'
        
        if answer_format == 'mcq':
            valid_options = set(options.keys()) if options else {'A', 'B', 'C', 'D'}
            if answer not in valid_options:
                answer = 'A'
        
        return answer
    
    def get_total_tokens(self) -> Tuple[int, int, int]:
        return self.llm_client.get_total_tokens()