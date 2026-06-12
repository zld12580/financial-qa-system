# 金融问答系统

基于DeepSeek大模型的金融文档问答系统，用于回答选择题并生成评测报告。

## 项目结构

```
qa_system/
├── config.py            # 配置文件
├── pdf_extractor.py     # PDF文档提取器
├── question_loader.py   # 问题加载器
├── deepseek_client.py   # DeepSeek API客户端
├── answer_generator.py  # 答案生成器
├── report_generator.py  # 报告生成器
├── main.py             # 主程序
├── output/             # 输出目录
└── requirements.txt    # 依赖包
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

API已在config.py中配置：
- API URL: https://llmapi.inner.sincetech.com/v1
- Model: deepseek-v4-flash
- API Key: sk-DJur0WvetsmCGN3IhHPYf9Dl184B2I3TEgwC1940rHqYIwXh

也可通过环境变量覆盖：

```bash
export DEEPSEEK_API_KEY="your_api_key"
export DEEPSEEK_API_URL="https://llmapi.inner.sincetech.com/v1"
export DEEPSEEK_MODEL="deepseek-v4-flash"
```

## 运行

```bash
python main.py
```

## 输出格式

生成 `output/answer.csv`，格式如下：

| qid | answer | prompt_tokens | completion_tokens | total_tokens |
|-----|--------|---------------|-------------------|--------------|
| summary | | 3627557 | 629 | 3628186 |
| ins_a_001 | B | 37201 | 1 | 37202 |

## Token优化策略

1. **PDF文本截断**: 每个PDF最多提取50页，总长度限制30k字符
2. **精准定位**: A组题目直接使用doc_ids定位文档，避免全库检索
3. **简洁Prompt**: 仅包含必要的问题、选项和关键上下文
4. **答案验证**: 自动验证答案格式，确保符合规范