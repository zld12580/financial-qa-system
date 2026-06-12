import csv
import os
from typing import List, Dict, Tuple
import config


class ReportGenerator:
    def __init__(self):
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    def generate(self, results: List[Dict], total_tokens: Tuple[int, int, int]) -> str:
        output_file = os.path.join(config.OUTPUT_DIR, "answer.csv")
        
        prompt_tokens, completion_tokens, total = total_tokens
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['qid', 'answer', 'prompt_tokens', 'completion_tokens', 'total_tokens'])
            
            writer.writerow([
                'summary',
                '',
                prompt_tokens,
                completion_tokens,
                total
            ])
            
            for result in results:
                writer.writerow([
                    result['qid'],
                    result['answer'],
                    result['prompt_tokens'],
                    result['completion_tokens'],
                    result['total_tokens']
                ])
        
        return output_file