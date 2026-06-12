import pdfplumber
import os
from typing import Dict, List
import config


class PDFExtractor:
    def __init__(self):
        self.cache: Dict[str, str] = {}
    
    def extract_text(self, domain: str, doc_id: str) -> str:
        cache_key = f"{domain}_{doc_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        domain_dir = os.path.join(config.RAW_DIR, domain)
        if not os.path.exists(domain_dir):
            return ""
        
        found_file = None
        file_type = None
        
        for root, dirs, files in os.walk(domain_dir):
            for file in files:
                file_lower = file.lower()
                file_id = os.path.splitext(file)[0]
                
                if file_id == doc_id:
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
            return ""
        
        if file_type == 'pdf':
            text = self._extract_from_pdf(found_file)
        elif file_type == 'html':
            text = self._extract_from_html(found_file)
        elif file_type == 'txt':
            text = self._extract_from_txt(found_file)
        else:
            text = ""
        
        self.cache[cache_key] = text
        return text
    
    def _extract_from_pdf(self, pdf_path: str) -> str:
        try:
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                pages_to_read = min(len(pdf.pages), config.MAX_PDF_PAGES)
                for i, page in enumerate(pdf.pages[:pages_to_read]):
                    page_text = page.extract_text()
                    if page_text:
                        page_text = page_text.strip()
                        page_text = ' '.join(page_text.split())
                        text_parts.append(f"[第{i+1}页]\n{page_text}")
            
            full_text = "\n\n".join(text_parts)
            if len(full_text) > config.MAX_CONTEXT_LENGTH:
                full_text = full_text[:config.MAX_CONTEXT_LENGTH]
            
            return full_text
        except Exception as e:
            print(f"PDF提取失败 {pdf_path}: {e}")
            return ""
    
    def _extract_from_html(self, html_path: str) -> str:
        try:
            from bs4 import BeautifulSoup
            
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            text = ' '.join(text.split())
            
            if len(text) > config.MAX_CONTEXT_LENGTH:
                text = text[:config.MAX_CONTEXT_LENGTH]
            
            return text
        except Exception as e:
            print(f"HTML提取失败 {html_path}: {e}")
            return ""
    
    def _extract_from_txt(self, txt_path: str) -> str:
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            text = ' '.join(text.split())
            
            if len(text) > config.MAX_CONTEXT_LENGTH:
                text = text[:config.MAX_CONTEXT_LENGTH]
            
            return text
        except Exception as e:
            print(f"TXT提取失败 {txt_path}: {e}")
            return ""
    
    def extract_multiple(self, domain: str, doc_ids: List[str]) -> str:
        texts = []
        for doc_id in doc_ids:
            text = self.extract_text(domain, doc_id)
            if text:
                texts.append(f"【文档{doc_id}】\n{text}")
        
        return "\n\n".join(texts)