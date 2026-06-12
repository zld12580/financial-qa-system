from typing import Tuple
import config


class DeepSeekClient:
    def __init__(self):
        self.api_key = config.DEEPSEEK_API_KEY
        self.api_url = config.DEEPSEEK_API_URL
        self.model = config.DEEPSEEK_MODEL
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
    
    def call(self, prompt: str) -> Tuple[str, int, int]:
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_url
            )
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.03,
                max_tokens=300,
                top_p=0.95,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            message = response.choices[0].message
            answer = message.content or ""
            
            if hasattr(message, 'reasoning_content') and message.reasoning_content:
                reasoning = message.reasoning_content
                import re
                matches = re.findall(r'\b([A-D])\b', reasoning)
                if matches:
                    answer = ''.join(matches)
                else:
                    answer = reasoning
            
            import re
            
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
                    answer = match.group(1)
                    break
            else:
                lines = answer.strip().split('\n')
                for line in reversed(lines):
                    line = line.strip()
                    if line and len(line) <= 10:
                        if re.match(r'^[A-D]+$', line):
                            answer = line
                            break
                        matches = re.findall(r'\b([A-D])\b', line)
                        if matches:
                            answer = ''.join(matches)
                            break
                
                if not answer or len(answer) > 4:
                    all_matches = re.findall(r'\b([A-D])\b', answer)
                    if all_matches:
                        answer = ''.join(all_matches)
            
            answer = answer.strip()
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            
            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            
            return answer, prompt_tokens, completion_tokens
            
        except Exception as e:
            print(f"DeepSeek API调用失败: {e}")
            return self._mock_call(prompt)
    
    def _mock_call(self, prompt: str) -> Tuple[str, int, int]:
        prompt_tokens = len(prompt) // 4
        completion_tokens = 1
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        return "A", prompt_tokens, completion_tokens
    
    def get_total_tokens(self) -> Tuple[int, int, int]:
        return (
            self.total_prompt_tokens,
            self.total_completion_tokens,
            self.total_prompt_tokens + self.total_completion_tokens
        )