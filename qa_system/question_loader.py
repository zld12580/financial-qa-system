import json
import os
from typing import List, Dict
import config


class QuestionLoader:
    def __init__(self):
        self.questions: List[Dict] = []
    
    def load_all(self) -> List[Dict]:
        self.questions = []
        
        for root, dirs, files in os.walk(config.QUESTIONS_DIR):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    self._load_file(file_path)
        
        return self.questions
    
    def _load_file(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.questions.extend(data)
                elif isinstance(data, dict):
                    self.questions.append(data)
        except Exception as e:
            print(f"加载问题文件失败 {file_path}: {e}")
    
    def get_by_qid(self, qid: str) -> Dict:
        for q in self.questions:
            if q.get('qid') == qid:
                return q
        return {}