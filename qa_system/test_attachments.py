import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_extractor import PDFExtractor

print("=" * 60)
print("测试regulatory/attachments/*.pdf提取")
print("=" * 60)

extractor = PDFExtractor()

test_cases = [
    ('regulatory', 'csrc_0001_att1'),
    ('regulatory', 'csrc_0001_att2'),
    ('regulatory', 'csrc_0002_att1'),
    ('regulatory', 'csrc_0043_att5'),
]

print("\n测试结果:")
for domain, doc_id in test_cases:
    text = extractor.extract_text(domain, doc_id)
    status = "✓" if len(text) > 0 else "✗"
    print(f"{status} {doc_id:20s} 长度: {len(text):6d} 字符")
    if text:
        print(f"   前80字符: {text[:80]}")

print("\n测试完成!")