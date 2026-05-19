# Development Log

## Day 1

完成内容：

- 创建 GitHub 仓库；
- 编写第一版 README.md；
- 将项目同步到 GitHub。

遇到的问题：

- Markdown 表格和代码块格式不熟悉；
- 本地目录和 GitHub 仓库同步流程不熟悉。

解决方式：

- 学会使用 `git add`、`git commit`、`git push`；
- 配置 Git 代理后成功推送到 GitHub。

---

## Day 2

完成内容：

- 建立项目基础目录；
- 创建 `requirements.txt`；
- 测试本地模型运行；
- 修复 PyTorch CPU 版问题；
- 安装 CUDA 版 PyTorch；
- 确认 RTX 4060 可以用于本地推理。

遇到的问题：

- 运行模型时报错：`Torch not compiled with CUDA enabled`；
- 原因是安装了 CPU 版 PyTorch。

解决方式：

- 使用以下命令重新安装 CUDA 版 PyTorch：

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
---
```

---

## Day 3

完成内容：

- 编写 `docs/system_design.md`；
- 明确当前 Baseline 系统流程；
- 明确最终系统流程：RAG + CoT + SymPy 自验证；
- 建立 `src/model_client.py`、`src/prompts.py`、`src/baseline_solver.py`、`src/evaluator.py` 等核心模块骨架；
- 将 Day 3 内容同步到 GitHub。

当前理解：

- Baseline 是后续所有方法的对照组；
- RAG、CoT、SymPy 都应该建立在 Baseline 流程之上；
- `model_client.py` 应该统一负责模型加载和生成，避免在多个文件中重复写模型调用代码；
- `prompts.py` 负责管理提示词模板；
- `baseline_solver.py` 负责读取题目、调用模型、保存结果；
- `evaluator.py` 后续负责判断答案是否正确。

遇到的问题：

- 暂无明显代码问题；
- 当前主要任务是把系统架构从想法变成可运行的代码结构。

下一步计划：

- 实现 `src/model_client.py`；
- 编写统一的本地模型调用函数；
- 测试输入一道数学题后，模型能返回答案。
