import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_extractor import PDFExtractor

print("=" * 60)
print("测试所有文档类型的提取功能")
print("=" * 60)

extractor = PDFExtractor()

test_cases = [
    ('financial_contracts', 'text01', 'PDF文档'),
    ('financial_reports', 'annual_byd_2024_report', 'PDF文档(大写扩展名)'),
    ('regulatory', 'strict_v3_008_中国人民银行令〔2025〕第12号（金融机构客户受益所有人识别管理办法）', 'TXT文档'),
    ('regulatory', 'csrc_0001', 'HTML文档'),
    ('regulatory', 'csrc_0001_att1', 'PDF附件'),
]

print("\n测试结果:")
for domain, doc_id, doc_type in test_cases:
    text = extractor.extract_text(domain, doc_id)
    status = "✓" if len(text) > 0 else "✗"
    print(f"{status} {doc_type:30s} 长度: {len(text):6d} 字符")

print("\n所有文档类型测试完成!")