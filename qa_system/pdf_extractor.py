"""
PDF/HTML/TXT文档提取器

支持从多种格式文档中提取文本内容，用于金融问答系统的参考资料提取。
"""

import pdfplumber
import os
from typing import Dict, List
import config


class PDFExtractor:
    """文档提取器，支持PDF、HTML、TXT格式"""
    
    def __init__(self):
        """初始化提取器，创建文本缓存"""
        self.cache: Dict[str, str] = {}
    
    def extract_text(self, domain: str, doc_id: str) -> str:
        """
        提取指定文档的文本内容
        
        Args:
            domain: 文档领域（如financial_contracts, regulatory等）
            doc_id: 文档ID（不含扩展名）
        
        Returns:
            提取的文本内容，如果未找到则返回空字符串
        
        Note:
            - 支持PDF、HTML、TXT三种格式
            - 自动递归搜索子目录
            - 使用缓存避免重复提取
        """
        cache_key = f"{domain}_{doc_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        domain_dir = os.path.join(config.RAW_DIR, domain)
        if not os.path.exists(domain_dir):
            print(f"警告: 领域目录不存在: {domain_dir}")
            return ""
        
        found_file = None
        file_type = None
        
        # 递归搜索所有子目录
        for root, dirs, files in os.walk(domain_dir):
            for file in files:
                file_lower = file.lower()
                file_id = os.path.splitext(file)[0]
                
                if file_id == doc_id:
                    # 按优先级匹配文件类型
                    if file_lower.endswith('.pdf'):
                        found_file = os.path.join(root, file)
                        file_type = 'pdf'
                        break
                    elif file_lower.endswith('.html'):
                        found_file = os.path.join(root, file)
                        file_type = 'html'
                        break
                    elif file_lower.endswith('.txt'):
                        found_file = os.path.join(root, file)
                        file_type = 'txt'
                        break
            if found_file:
                break
        
        if not found_file:
            print(f"警告: 未找到文档: {domain}/{doc_id}")
            return ""
        
        # 根据文件类型调用对应的提取方法
        try:
            if file_type == 'pdf':
                text = self._extract_from_pdf(found_file)
            elif file_type == 'html':
                text = self._extract_from_html(found_file)
            elif file_type == 'txt':
                text = self._extract_from_txt(found_file)
            else:
                text = ""
        except Exception as e:
            print(f"错误: 文档提取失败 {found_file}: {e}")
            text = ""
        
        self.cache[cache_key] = text
        return text
    
    def _extract_from_pdf(self, pdf_path: str) -> str:
        """
        从PDF文件提取文本
        
        Args:
            pdf_path: PDF文件路径
        
        Returns:
            提取的文本内容
        
        Note:
            - 限制读取页数（由config.MAX_PDF_PAGES控制）
            - 限制文本长度（由config.MAX_CONTEXT_LENGTH控制）
            - 自动清理多余空白字符
        """
        try:
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                pages_to_read = min(len(pdf.pages), config.MAX_PDF_PAGES)
                for i, page in enumerate(pdf.pages[:pages_to_read]):
                    page_text = page.extract_text()
                    if page_text:
                        page_text = page_text.strip()
                        page_text = ' '.join(page_text.split())  # 清理多余空白
                        text_parts.append(f"[第{i+1}页]\n{page_text}")
            
            full_text = "\n\n".join(text_parts)
            
            # 限制文本长度
            if len(full_text) > config.MAX_CONTEXT_LENGTH:
                full_text = full_text[:config.MAX_CONTEXT_LENGTH]
                print(f"提示: PDF文本已截断至{config.MAX_CONTEXT_LENGTH}字符")
            
            return full_text
        except Exception as e:
            print(f"PDF提取失败 {pdf_path}: {e}")
            return ""
    
    def _extract_from_html(self, html_path: str) -> str:
        """
        从HTML文件提取文本
        
        Args:
            html_path: HTML文件路径
        
        Returns:
            提取的文本内容
        
        Note:
            - 自动移除script和style标签
            - 尝试多种编码方式读取
        """
        try:
            from bs4 import BeautifulSoup
            
            # 尝试多种编码
            html_content = None
            for encoding in ['utf-8', 'gbk', 'gb2312', 'latin1']:
                try:
                    with open(html_path, 'r', encoding=encoding) as f:
                        html_content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if html_content is None:
                print(f"错误: 无法解码HTML文件 {html_path}")
                return ""
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 移除脚本和样式
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            text = ' '.join(text.split())  # 清理多余空白
            
            # 限制文本长度
            if len(text) > config.MAX_CONTEXT_LENGTH:
                text = text[:config.MAX_CONTEXT_LENGTH]
            
            return text
        except Exception as e:
            print(f"HTML提取失败 {html_path}: {e}")
            return ""
    
    def _extract_from_txt(self, txt_path: str) -> str:
        """
        从TXT文件提取文本
        
        Args:
            txt_path: TXT文件路径
        
        Returns:
            提取的文本内容
        
        Note:
            - 尝试多种编码方式读取
            - 自动清理多余空白字符
        """
        try:
            # 尝试多种编码
            text = None
            for encoding in ['utf-8', 'gbk', 'gb2312', 'latin1']:
                try:
                    with open(txt_path, 'r', encoding=encoding) as f:
                        text = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if text is None:
                print(f"错误: 无法解码TXT文件 {txt_path}")
                return ""
            
            text = ' '.join(text.split())  # 清理多余空白
            
            # 限制文本长度
            if len(text) > config.MAX_CONTEXT_LENGTH:
                text = text[:config.MAX_CONTEXT_LENGTH]
            
            return text
        except Exception as e:
            print(f"TXT提取失败 {txt_path}: {e}")
            return ""
    
    def extract_multiple(self, domain: str, doc_ids: List[str]) -> str:
        """
        批量提取多个文档的文本内容
        
        Args:
            domain: 文档领域
            doc_ids: 文档ID列表
        
        Returns:
            合并后的文本内容，每个文档用分隔符标记
        """
        texts = []
        for doc_id in doc_ids:
            text = self.extract_text(domain, doc_id)
            if text:
                texts.append(f"【文档{doc_id}】\n{text}")
        
        return "\n\n".join(texts)
