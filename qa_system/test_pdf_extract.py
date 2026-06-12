import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_extractor import PDFExtractor

extractor = PDFExtractor()

test_cases = [
    ('financial_reports', 'annual_byd_2024_report'),
    ('financial_reports', 'annual_catl_2024_report'),
    ('financial_contracts', 'text01'),
]

for domain, doc_id in test_cases:
    text = extractor.extract_text(domain, doc_id)
    print(f"\n{domain}/{doc_id}:")
    print(f"  文本长度: {len(text)}")
    if text:
        print(f"  前100字符: {text[:100]}")
    else:
        print(f"  未找到文档!")