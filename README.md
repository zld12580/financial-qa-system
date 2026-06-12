# 金融文档智能问答系统

基于DeepSeek大模型的金融文档问答系统，用于回答金融领域的多选题、判断题，并生成评测报告。

## 项目简介

本系统是一个针对金融领域文档的智能问答系统，能够：
- 自动提取PDF、HTML、TXT等多种格式文档内容
- 基于DeepSeek大模型进行智能推理
- 支持单选题、多选题、判断题等多种题型
- 生成详细的评测报告和答案分布统计

## 项目结构

```
├── public_dataset_upload/       # 数据集目录
│   ├── questions/              # 问题数据
│   │   └── group_a/           # A组题目
│   │       ├── financial_contracts_questions.json
│   │       ├── financial_reports_questions.json
│   │       ├── insurance_questions.json
│   │       ├── regulatory_questions.json
│   │       └── research_questions.json
│   └── raw/                    # 原始文档
│       ├── financial_contracts/  # 金融合同文档
│       ├── financial_reports/    # 财务报告文档
│       ├── insurance/           # 保险文档
│       ├── regulatory/          # 监管文档
│       │   ├── attachments/    # PDF附件
│       │   ├── html/           # HTML文档
│       │   └── txt/            # TXT文档
│       └── research/           # 研究报告文档
├── qa_system/                  # 核心代码
│   ├── config.py              # 配置管理
│   ├── pdf_extractor.py       # 文档提取器
│   ├── question_loader.py     # 问题加载器
│   ├── deepseek_client.py     # DeepSeek API客户端
│   ├── answer_generator.py    # 答案生成器
│   ├── report_generator.py    # 报告生成器
│   ├── main.py                # 主程序
│   ├── run_batch.py           # 批量处理脚本
│   ├── output/                # 输出目录
│   └── requirements.txt       # 依赖包
├── .env.example               # 环境变量示例
├── .gitignore                 # Git忽略文件
└── README.md                  # 项目说明文档
```

## 功能特性

### 1. 多格式文档支持
- **PDF文档**：支持大小写扩展名（.pdf/.PDF）
- **HTML文档**：使用BeautifulSoup4解析
- **TXT文档**：纯文本文件
- **递归搜索**：自动搜索子目录中的文档

### 2. 智能问答
- **单选题**：唯一正确答案推理
- **多选题**：多选项验证与选择
- **判断题**：陈述正确性判断
- **基于文档**：严格基于参考资料回答

### 3. 优化的Prompt设计
- 详细的分步推理说明
- 具体的示例演示
- 强调基于资料明确依据
- 针对不同题型定制策略

### 4. 答案验证
- 格式规范化
- 多选题答案限制
- 选项有效性检查

## 安装说明

### 1. 克隆仓库
```bash
git clone <repository-url>
cd 000-aliyun-test
```

### 2. 安装依赖
```bash
pip install -r qa_system/requirements.txt
```

### 3. 配置环境变量
```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑.env文件，填入你的API配置
# DEEPSEEK_API_KEY=your_api_key_here
# DEEPSEEK_API_URL=your_api_Url_here
# DEEPSEEK_MODEL=DeepSeek-V4-Flash
```

## 使用方法

### 快速开始

```bash
# 运行主程序（处理所有题目）
python qa_system/main.py

# 批量处理
python qa_system/run_batch.py

# 增量处理（支持断点续传）
python qa_system/run_incremental.py
```

### 测试脚本

```bash
# 测试前20题
python qa_system/test_20.py

# 快速测试前10题
python qa_system/test_quick.py

# 测试文档提取功能
python qa_system/test_pdf_extract.py
python qa_system/test_all_types.py
```

## 输出格式

生成的答案文件位于 `qa_system/output/answer.csv`，格式如下：

| 字段 | 说明 |
|------|------|
| qid | 问题ID |
| answer | 答案（如A、AB、ABCD等） |
| prompt_tokens | 输入token数 |
| completion_tokens | 输出token数 |
| total_tokens | 总token数 |

示例：
| qid | answer | prompt_tokens | completion_tokens | total_tokens |
| fc_a_001 | ABD | 12648 | 300 | 12948 |
| fc_a_002 | ABD | 12642 | 300 | 12942 |
| fc_a_003 | A | 12597 | 174 | 12771 |


## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| DEEPSEEK_API_KEY | DeepSeek API密钥 | - |
| DEEPSEEK_API_URL | API地址 | - |
| DEEPSEEK_MODEL | 模型名称 | DeepSeek-V4-Flash |

### 系统参数

在 `qa_system/config.py` 中可调整：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| MAX_PDF_PAGES | PDF最大读取页数 | 35 |
| MAX_CONTEXT_LENGTH | 最大上下文长度 | 25000 |

## 技术架构

### 核心模块

#### 1. PDFExtractor (pdf_extractor.py)
- 支持PDF/HTML/TXT多格式文档提取
- 递归搜索子目录
- 文档内容缓存机制
- 大小写不敏感的文件匹配

#### 2. QuestionLoader (question_loader.py)
- 加载JSON格式的问题数据
- 支持多个领域的问题集
- 自动合并所有问题

#### 3. DeepSeekClient (deepseek_client.py)
- DeepSeek API封装
- 答案提取与解析
- Token消耗统计
- 错误处理与重试

#### 4. AnswerGenerator (answer_generator.py)
- 构建优化的Prompt
- 调用大模型生成答案
- 答案验证与规范化
- 支持多种题型

### 数据流程

```
问题加载 → 文档提取 → Prompt构建 → 模型推理 → 答案提取 → 结果验证 → 输出保存
```

## 性能优化

### 1. Token优化
- PDF文本截断（最多35页）
- 上下文长度限制（25k字符）
- 文档内容缓存

### 2. 文档定位
- 精准使用doc_ids定位文档
- 避免全库检索
- 递归搜索子目录

### 3. Prompt优化
- 简洁明确的问题描述
- 必要的上下文信息
- 分步推理指导

## 常见问题

### Q1: 为什么某些题目token消耗很少？
A: 可能原因：
- 文档扩展名大小写不匹配（已修复）
- 文档路径配置错误
- 文档不存在

### Q2: 如何处理regulatory目录的文档？
A: regulatory目录有特殊结构：
- `attachments/` - PDF附件
- `html/` - HTML文档
- `txt/` - TXT文档
系统会自动递归搜索这些子目录。

### Q3: 如何添加新的文档类型？
A: 在`pdf_extractor.py`中添加新的提取方法，并在`extract_text()`中添加对应的文件类型判断。

## 开发指南

### 添加新的问题领域

1. 在`public_dataset_upload/questions/group_a/`添加JSON文件
2. 在`public_dataset_upload/raw/`创建对应目录
3. 放入相关文档

### 自定义Prompt模板

修改`answer_generator.py`中的`_build_prompt()`方法。

### 调整模型参数

修改`deepseek_client.py`中的API调用参数：
- temperature
- max_tokens
- top_p

## 依赖说明

主要依赖包：
- `openai` - OpenAI API客户端
- `pdfplumber` - PDF文本提取
- `beautifulsoup4` - HTML解析
- `python-dotenv` - 环境变量管理
- `pandas` - 数据处理
- `tqdm` - 进度条显示

## 许可证

本项目仅供学习和研究使用。

## 贡献指南

欢迎提交Issue和Pull Request。

## 更新日志

### v1.0.0 (2026-06-12)
- 初始版本发布
- 支持多格式文档提取
- 实现智能问答功能
- 优化Prompt设计
- 修复PDF扩展名大小写问题
- 支持regulatory目录特殊结构