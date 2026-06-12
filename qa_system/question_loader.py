"""
问题加载器

从JSON文件加载金融问答题目。
"""

import json
import os
from typing import List, Dict
import config


class QuestionLoader:
    """问题加载器，从文件系统加载问题数据"""
    
    def __init__(self):
        """初始化加载器"""
        self.questions: List[Dict] = []
    
    def load_all(self) -> List[Dict]:
        """
        加载所有问题
        
        Returns:
            问题列表，每个问题是一个字典
        
        Note:
            - 递归搜索questions目录下的所有JSON文件
            - 自动合并所有问题到单一列表
        """
        self.questions = []
        
        if not os.path.exists(config.QUESTIONS_DIR):
            print(f"错误: 问题目录不存在: {config.QUESTIONS_DIR}")
            return []
        
        for root, dirs, files in os.walk(config.QUESTIONS_DIR):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    self._load_file(file_path)
        
        print(f"成功加载 {len(self.questions)} 道题目")
        return self.questions
    
    def _load_file(self, file_path: str):
        """
        加载单个JSON文件
        
        Args:
            file_path: JSON文件路径
        
        Note:
            支持JSON数组或单个对象
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.questions.extend(data)
                elif isinstance(data, dict):
                    self.questions.append(data)
        except json.JSONDecodeError as e:
            print(f"JSON解析失败 {file_path}: {e}")
        except Exception as e:
            print(f"加载问题文件失败 {file_path}: {e}")
    
    def get_by_qid(self, qid: str) -> Dict:
        """
        根据问题ID获取问题
        
        Args:
            qid: 问题ID
        
        Returns:
            问题字典，如果未找到返回空字典
        
        Warning:
            必须先调用load_all()加载数据
        """
        if not self.questions:
            print("警告: 问题列表为空，请先调用load_all()")
            return {}
        
        for q in self.questions:
            if q.get('qid') == qid:
                return q
        
        print(f"警告: 未找到问题 {qid}")
        return {}
    
    def get_by_domain(self, domain: str) -> List[Dict]:
        """
        根据领域获取问题列表
        
        Args:
            domain: 领域名称
        
        Returns:
            该领域的所有问题
        """
        if not self.questions:
            print("警告: 问题列表为空，请先调用load_all()")
            return []
        
        return [q for q in self.questions if q.get('domain') == domain]
    
    def get_statistics(self) -> Dict:
        """
        获取问题统计信息
        
        Returns:
            统计信息字典，包含总数和各领域数量
        """
        if not self.questions:
            return {"total": 0}
        
        stats = {"total": len(self.questions)}
        
        # 统计各领域数量
        domain_counts = {}
        for q in self.questions:
            domain = q.get('domain', 'unknown')
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        stats["domains"] = domain_counts
        
        # 统计各题型数量
        format_counts = {}
        for q in self.questions:
            fmt = q.get('answer_format', 'unknown')
            format_counts[fmt] = format_counts.get(fmt, 0) + 1
        
        stats["formats"] = format_counts
        
        return stats
