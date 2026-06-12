# 变更日志

所有重要的变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-06-12

### 新增
- 初始版本发布
- 支持PDF、HTML、TXT多格式文档提取
- 实现基于DeepSeek大模型的智能问答
- 支持单选题、多选题、判断题
- 添加环境变量配置支持
- 添加详细的README文档
- 添加贡献指南和许可证

### 优化
- 优化Prompt模板设计
  - 添加详细的分步推理说明
  - 添加具体示例演示
  - 强调基于资料明确依据
- 优化答案提取逻辑
  - 简化正则表达式
  - 改进多选题答案验证
- Token使用优化
  - PDF文本截断（最多35页）
  - 上下文长度限制（25k字符）
  - 文档内容缓存机制

### 修复
- 修复PDF扩展名大小写不匹配问题
  - 使用大小写不敏感的文件匹配
  - 解决`.PDF`和`.pdf`扩展名问题
- 修复regulatory目录文档提取问题
  - 支持递归搜索子目录
  - 正确处理attachments、html、txt子目录
- 修复API模型名称配置错误
  - 从`deepseek-v4-flash`改为`DeepSeek-V4-Flash`

### 文档
- 完善README.md
- 添加CONTRIBUTING.md
- 添加LICENSE
- 添加CHANGELOG.md
- 添加.env.example

## [0.1.0] - 2026-06-11

### 新增
- 项目初始化
- 基础代码结构搭建
- PDF提取功能
- 问题加载功能
- DeepSeek API集成