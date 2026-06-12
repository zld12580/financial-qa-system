import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_extractor import PDFExtractor

extractor = PDFExtractor()

test_cases = [
    ('regulatory', 'strict_v3_008_中国人民银行令〔2025〕第12号（金融机构客户受益所有人识别管理办法）'),
    ('regulatory', 'csrc_0001'),
    ('regulatory', 'csrc_0001_att1'),
]

for domain, doc_id in test_cases:
    text = extractor.extract_text(domain, doc_id)
    print(f"\n{domain}/{doc_id}:")
    print(f"  文本长度: {len(text)}")
    if text:
        print(f"  前100字符: {text[:100]}")
    else:
        print(f"  未找到文档!")