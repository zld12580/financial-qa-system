"""
答案生成器

基于DeepSeek大模型生成金融问题的答案。
"""

from typing import Dict, Tuple
from pdf_extractor import PDFExtractor
from deepseek_client import DeepSeekClient


class AnswerGenerator:
    """答案生成器，协调文档提取和模型推理"""
    
    def __init__(self):
        """初始化生成器，创建提取器和客户端"""
        self.pdf_extractor = PDFExtractor()
        self.llm_client = DeepSeekClient()
    
    def generate(self, question: Dict) -> Tuple[str, int, int]:
        """
        生成单个问题的答案
        
        Args:
            question: 问题字典，包含qid、domain、question、options等字段
        
        Returns:
            (答案, 输入token数, 输出token数)
        
        Note:
            完整流程：提取文档 → 构建prompt → 模型推理 → 验证答案
        """
        qid = question.get('qid', '')
        domain = question.get('domain', '')
        question_text = question.get('question', '')
        options = question.get('options', {})
        answer_format = question.get('answer_format', 'mcq')
        doc_ids = question.get('doc_ids', [])
        
        # 提取参考文档
        context = ""
        if doc_ids:
            context = self.pdf_extractor.extract_multiple(domain, doc_ids)
            if not context:
                print(f"警告: 问题{qid}未提取到参考文档")
        
        # 构建提示词
        prompt = self._build_prompt(question_text, options, answer_format, context)
        
        # 调用模型生成答案
        answer, prompt_tokens, completion_tokens = self.llm_client.call(prompt)
        
        # 验证并规范化答案
        answer = self._validate_answer(answer, answer_format, options)
        
        return answer, prompt_tokens, completion_tokens
    
    def _build_prompt(self, question: str, options: Dict, answer_format: str, context: str) -> str:
        """
        构建提示词
        
        Args:
            question: 问题文本
            options: 选项字典
            answer_format: 答案格式（mcq/tf/multi）
            context: 参考文档内容
        
        Returns:
            完整的提示词
        
        Note:
            针对不同题型构建不同的推理指导
        """
        prompt_parts = []
        
        # 添加参考资料
        if context:
            prompt_parts.append(f"参考资料：\n{context}\n")
            prompt_parts.append("=" * 50)
            prompt_parts.append("【重要】必须严格基于上述参考资料回答，不得使用外部知识或主观推断。\n")
        
        # 添加问题
        prompt_parts.append(f"问题：{question}\n")
        
        # 添加选项
        if options:
            prompt_parts.append("选项：")
            for key in sorted(options.keys()):
                prompt_parts.append(f"{key}. {options[key]}")
            prompt_parts.append("")
        
        # 根据题型添加推理指导
        if answer_format == 'mcq':
            prompt_parts.extend(self._build_mcq_prompt())
        elif answer_format == 'tf':
            prompt_parts.extend(self._build_tf_prompt())
        elif answer_format == 'multi':
            prompt_parts.extend(self._build_multi_prompt())
        
        return "\n".join(prompt_parts)
    
    def _build_mcq_prompt(self) -> list:
        """构建单选题提示词"""
        return [
            "【任务】单选题 - 选择唯一正确答案",
            "\n【分析方法】",
            "步骤1：仔细阅读问题，理解考查的核心要点",
            "步骤2：对每个选项逐一验证：",
            "  - 在参考资料中查找该选项对应的具体内容",
            "  - 判断该内容是否与选项描述完全一致",
            "  - 标记为'符合'或'不符合'",
            "步骤3：排除所有不符合的选项",
            "步骤4：确认唯一符合的选项作为答案",
            "\n【重要提示】",
            "1. 必须在资料中找到明确的文字依据",
            "2. 不能根据常识或推断选择",
            "3. 如果多个选项看似合理，选择资料中明确提到的",
            "\n【示例】",
            "问题：发行人名称是什么？",
            "选项：A.张三公司 B.李四公司 C.王五公司 D.赵六公司",
            "分析：查阅资料第X页，发行人明确写为'李四公司'，故A/C/D不符合，B符合",
            "答案：B",
            "\n请严格按照上述格式回答：",
            "分析：[逐项验证过程]",
            "答案：[单个字母]"
        ]
    
    def _build_tf_prompt(self) -> list:
        """构建判断题提示词"""
        return [
            "【任务】判断题 - 判断陈述是否正确",
            "\n【分析方法】",
            "步骤1：提取陈述中的关键信息和数据",
            "步骤2：在参考资料中定位相关内容",
            "步骤3：逐项对比陈述与资料",
            "  - 完全一致 → 正确(A)",
            "  - 存在差异 → 错误(B)",
            "步骤4：做出明确判断",
            "\n【示例】",
            "陈述：发行金额为10亿元",
            "分析：查阅资料第Y页，发行金额明确写为'15亿元'，与陈述不符",
            "答案：B",
            "\n请严格按照上述格式回答：",
            "分析：[对比过程]",
            "答案：[A=正确，B=错误]"
        ]
    
    def _build_multi_prompt(self) -> list:
        """构建多选题提示词"""
        return [
            "【任务】多选题 - 选择所有正确答案",
            "\n【分析方法】",
            "步骤1：理解问题的考查范围",
            "步骤2：对每个选项独立验证：",
            "  - 在资料中查找明确依据",
            "  - 有明确依据 → 选中",
            "  - 无明确依据或与资料不符 → 不选",
            "步骤3：汇总所有有依据的选项",
            "步骤4：注意：宁缺毋滥，不确定的选项不要选",
            "\n【示例】",
            "问题：以下哪些描述正确？",
            "选项：A.金额10亿 B.评级AAA C.期限5年 D.利率4%",
            "分析：",
            "  A: 资料显示金额15亿，不符合",
            "  B: 资料显示评级AA+，不符合",
            "  C: 资料显示期限5年，符合",
            "  D: 资料显示利率4%，符合",
            "答案：CD",
            "\n请严格按照上述格式回答：",
            "分析：[逐项验证]",
            "答案：[按字母顺序，如ABC]"
        ]
    
    def _validate_answer(self, answer: str, answer_format: str, options: Dict) -> str:
        """
        验证并规范化答案
        
        Args:
            answer: 原始答案
            answer_format: 答案格式
            options: 选项字典
        
        Returns:
            规范化后的答案
        
        Note:
            - 过滤非法字符
            - 确保答案格式正确
            - 多选题去重并排序
        """
        # 转大写并去除空格
        answer = answer.upper().strip()
        
        # 过滤非法字符，只保留ABCD
        valid_chars = set("ABCD")
        answer = ''.join(c for c in answer if c in valid_chars)
        
        # 根据题型验证
        if answer_format == 'multi':
            # 多选题：去重并排序
            answer = ''.join(sorted(set(answer)))
            if not answer:
                answer = 'A'  # 默认答案
            elif len(answer) == 4:
                # 如果全选，可能有问题，取前2个
                answer = answer[:2]
                print(f"提示: 多选题答案为ABCD，已截断为前2个选项")
        elif answer_format in ['mcq', 'tf']:
            # 单选题/判断题：只取第一个字符
            if answer:
                answer = answer[0]
            else:
                answer = 'A'  # 默认答案
        
        # 判断题特殊验证
        if answer_format == 'tf' and answer not in ['A', 'B']:
            answer = 'A'
            print(f"警告: 判断题答案必须为A或B，已重置为A")
        
        # 单选题选项验证
        if answer_format == 'mcq':
            valid_options = set(options.keys()) if options else {'A', 'B', 'C', 'D'}
            if answer not in valid_options:
                print(f"警告: 答案{answer}不在有效选项{valid_options}中，已重置为A")
                answer = 'A'
        
        return answer
    
    def get_total_tokens(self) -> Tuple[int, int, int]:
        """
        获取累计token消耗
        
        Returns:
            (总输入token, 总输出token, 总token)
        """
        return self.llm_client.get_total_tokens()
