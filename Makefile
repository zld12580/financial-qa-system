.PHONY: install run test clean help

# 金融问答系统 Makefile

help:
	@echo "金融问答系统 - 可用命令:"
	@echo "  make install    - 安装依赖"
	@echo "  make run        - 运行主程序"
	@echo "  make test       - 运行测试"
	@echo "  make clean      - 清理输出文件"
	@echo "  make example    - 运行示例"

install:
	@echo "安装依赖..."
	pip install -r qa_system/requirements.txt

run:
	@echo "运行主程序..."
	python qa_system/main.py

test:
	@echo "运行测试..."
	python qa_system/test_20.py

clean:
	@echo "清理输出文件..."
	rm -rf qa_system/output/*.csv
	rm -rf __pycache__
	rm -rf qa_system/__pycache__

example:
	@echo "运行示例..."
	python examples.py

batch:
	@echo "批量处理..."
	python qa_system/run_batch.py