"""
DeepSeek API客户端

封装DeepSeek大模型API调用，提供问答推理功能。
"""

import re
from typing import Tuple
import config


class DeepSeekClient:
    """DeepSeek API客户端"""
    
    def __init__(self):
        """初始化客户端，加载配置"""
        self.api_key = config.DEEPSEEK_API_KEY
        self.api_url = config.DEEPSEEK_API_URL
        self.model = config.DEEPSEEK_MODEL
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        
        # 验证API配置
        if not self.api_key:
            print("警告: DEEPSEEK_API_KEY未配置，将使用mock模式")
    
    def call(self, prompt: str) -> Tuple[str, int, int]:
        """
        调用DeepSeek API生成答案
        
        Args:
            prompt: 输入提示词
        
        Returns:
            (答案, 输入token数, 输出token数)
        
        Note:
            - 使用低temperature确保结果稳定
            - 自动提取答案中的选项字母
            - 失败时自动降级到mock模式
        """
        # 如果API_KEY未配置，直接使用mock
        if not self.api_key:
            return self._mock_call(prompt)
        
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_url
            )
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.03,  # 低温度确保稳定
                max_tokens=300,
                top_p=0.95,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            message = response.choices[0].message
            answer = message.content or ""
            
            # 处理推理内容（如果模型返回了推理过程）
            if hasattr(message, 'reasoning_content') and message.reasoning_content:
                reasoning = message.reasoning_content
                matches = re.findall(r'\b([A-D])\b', reasoning)
                if matches:
                    answer = ''.join(matches)
                else:
                    answer = reasoning
            
            # 提取答案
            answer = self._extract_answer(answer)
            
            # 统计token
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            
            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            
            return answer, prompt_tokens, completion_tokens
            
        except Exception as e:
            print(f"DeepSeek API调用失败: {e}")
            return self._mock_call(prompt)
    
    def _extract_answer(self, answer: str) -> str:
        """
        从模型输出中提取答案选项
        
        Args:
            answer: 模型原始输出
        
        Returns:
            提取的答案（如A、AB、ABCD等）
        
        Note:
            - 优先匹配标准格式"答案：X"
            - 支持多种答案表达方式
            - 从最后一行反向搜索
        """
        # 标准答案格式匹配
        answer_patterns = [
            r'答案[：:]\s*([A-D]+)',
            r'答案是为\s*([A-D]+)',
            r'选择[：:]\s*([A-D]+)',
            r'正确答案[：:]\s*([A-D]+)',
            r'最终答案[：:]\s*([A-D]+)',
        ]
        
        for pattern in answer_patterns:
            match = re.search(pattern, answer)
            if match:
                return match.group(1)
        
        # 从最后一行反向搜索
        lines = answer.strip().split('\n')
        for line in reversed(lines):
            line = line.strip()
            if line and len(line) <= 10:
                # 直接匹配纯字母答案
                if re.match(r'^[A-D]+$', line):
                    return line
                # 提取行中的字母
                matches = re.findall(r'\b([A-D])\b', line)
                if matches:
                    return ''.join(matches)
        
        # 最后尝试从全文提取
        if not answer or len(answer) > 4:
            all_matches = re.findall(r'\b([A-D])\b', answer)
            if all_matches:
                return ''.join(all_matches)
        
        return answer.strip()
    
    def _mock_call(self, prompt: str) -> Tuple[str, int, int]:
        """
        Mock调用（API不可用时的降级方案）
        
        Args:
            prompt: 输入提示词
        
        Returns:
            (默认答案'A', 估算的token数)
        
        Warning:
            仅用于测试和降级，不应在生产环境依赖
        """
        prompt_tokens = len(prompt) // 4  # 粗略估算
        completion_tokens = 1
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        print("警告: 使用mock模式，返回默认答案'A'")
        return "A", prompt_tokens, completion_tokens
    
    def get_total_tokens(self) -> Tuple[int, int, int]:
        """
        获取累计token消耗
        
        Returns:
            (总输入token, 总输出token, 总token)
        """
        return (
            self.total_prompt_tokens,
            self.total_completion_tokens,
            self.total_prompt_tokens + self.total_completion_tokens
        )
