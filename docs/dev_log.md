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

---

## Day 4

完成内容

- 实现 `src/model_client.py`
- 使用 `LocalModelClient` 封装本地模型调用
- 成功调用本地模型 `Qwen/Qwen2.5-1.5B-Instruct`
- 使用一元二次方程测试模型输出

测试命令

```bash
python src/model_client.py
```

或使用测试文件运行：

```bash
python -m tests.test_model_client
```

测试题目

```text
解方程：x^2 - 5x + 6 = 0
```

测试结果

模型可以正常加载并生成答案。

在部分情况下，模型能够给出正确结果：

```text
x = 2 或 x = 3
```

但由于当前使用的是轻量级本地模型，数学推理结果有时不够稳定。

当前理解

- `model_client.py` 是统一的模型调用模块
- 后续 Baseline、RAG、CoT 都会复用该模块
- `tests/` 目录用于存放测试代码
- 测试文件的作用是验证功能是否被改坏
- 当前项目已经从临时 demo 进入可复用模块阶段

项目结构调整

新增文件：

```text
src/__init__.py
tests/__init__.py
```

作用：

- 让 `src` 成为 Python 包
- 让 `tests` 成为 Python 包
- 支持使用模块方式运行测试

例如：

```bash
python -m tests.test_model_client
```

初步原因分析

当前数学结果不稳定，可能原因包括：

- 模型较小：`Qwen/Qwen2.5-1.5B-Instruct`
- 当前 Prompt 较简单
- 生成参数存在随机性
- 小模型在数学推理任务上本身存在不稳定性

下一步计划

- 编写 `src/prompts.py`
- 将 Prompt 模板从模型调用代码中拆分出来
- 使用更稳定的生成参数，例如 `do_sample=False`
- 后续使用 SymPy 对计算结果进行校验
- 在 Baseline 阶段记录模型错误
- 为后续 RAG 和自验证方法提供对比

---

## Day 5

完成内容：

- 编写 `src/prompts.py`；
- 实现 Basic Prompt、CoT Prompt 和 Answer Only Prompt；
- 编写 `tests/test_prompts.py`；
- 编写 `tests/test_prompt_with_model.py`；
- 使用模型测试 Basic Prompt 和 CoT Prompt 的输出效果；
- 优化 `model_client.py`，使其只返回模型新生成的内容，而不是返回完整 Prompt + 回答。

遇到的问题：

- 初始输出中包含了原始 Prompt；
- 原因是 `tokenizer.decode(outputs[0])` 会把输入和输出一起解码；
- 修改时出现了 `return outside function` 报错；
- 原因是 `generate()` 函数缩进错误，被写进了 `__init__()` 内部。

解决方式：

- 使用输入 token 长度 `input_length` 截取模型新生成部分；
- 调整 `generate()` 函数缩进，使其和 `__init__()` 处于同一级；
- 将默认 `max_new_tokens` 调整为 512；
- 默认使用 `do_sample=False`，让数学解题输出更稳定。

当前理解：

- `prompts.py` 负责管理提示词模板；
- `model_client.py` 负责统一模型调用；
- 测试文件用于验证模块是否正常工作；
- CoT Prompt 可以让模型更倾向于输出分步骤推理；
- Prompt 能影响输出结构，但不能保证答案一定正确。

下一步计划：

- 创建 `data/test_questions.jsonl`；
- 准备第一批数学题；
- 为后续 Baseline 批量解题做准备。

---

## Day 6

完成内容：

- 创建 `data/test_questions.jsonl`；
- 准备第一批 10 道基础数学测试题；
- 覆盖代数方程、代数化简、导数、积分、极限、数列、概率和几何；
- 编写 `tests/test_load_questions.py`；
- 成功读取并打印 10 道测试题。

测试命令：

```bash
python tests/test_load_questions.py
```

测试结果：

```text
Loaded 10 questions.
```

当前理解：

- .jsonl 文件适合存储多条结构化数据；
- 当前每一行代表一道数学题；
- question 是模型需要解答的题目；
- answer 是后续评测时使用的标准答案；
- 当前测试只是验证数据读取，不是模型解题。

下一步计划：

- 编写 src/baseline_solver.py；
- 批量读取测试题；
- 调用 LocalModelClient 解题；
- 将模型输出保存到 results/baseline_results.jsonl。

---

## Day 7

完成内容：

- 编写 `src/baseline_solver.py`；
- 实现 `load_questions()` 函数，用于读取 JSONL 数学题数据；
- 实现 `save_result()` 函数，用于保存模型输出；
- 实现 `run_baseline()` 函数，用于批量调用模型解题；
- 使用 Basic Prompt 对前 3 道数学题进行 Baseline 测试；
- 成功生成 `results/baseline_results.jsonl`。

测试命令：

```bash
python -m src.baseline_solver
```

输出文件：

```text
results/baseline_results.jsonl
```

当前理解：

- baseline_solver.py 是第一版完整解题流程；
- 当前 Baseline 不使用 RAG、不使用 CoT、不使用 SymPy；
- Baseline 的作用是作为后续方法的对照组；
- 先保存模型原始输出，再单独写 evaluator 判断答案是否正确；
- 批量实验结果应该保存到 results/ 目录，而不是只打印在终端里。

下一步计划：

- 扩展 Baseline 运行到全部 10 道题；
- 编写 src/evaluator.py；
- 初步判断模型答案是否正确；
- 生成第一版 Baseline 分析报告。

补充测试：

- 将 `run_baseline(max_questions=3)` 修改为 `run_baseline(max_questions=None)`；
- 成功运行全部 10 道数学题；
- 成功生成完整的 `results/baseline_results.jsonl`。

观察结果：

- 本地模型可以完成批量解题；
- 运行速度较慢，但流程完整；
- 当前结果尚未自动判断正确性；
- 下一步需要编写 `evaluator.py` 对模型输出进行评测。

---

## Day 8

完成内容：

- 编写 `src/evaluator.py`
- 实现 `load_jsonl()` 和 `save_jsonl()`
- 实现 `normalize_text()`
- 实现第一版 `simple_match()`
- 对 `results/baseline_results.jsonl`进行初步评测
- 生成 `results/baseline_evaluated.jsonl`


测试命令：

```bash
python -m src.evaluator
```

输出文件：

```text
results/baseline_evaluated.jsonl
```

当前理解：
- 第一版 evaluator 使用简单字符串匹配；
- 该方法只能判断部分明显正确的答案；
- 对于等价表达式、答案顺序变化、格式不同等情况，简单匹配可能误判；
- 后续需要使用 SymPy 进行更可靠的数学等价判断。

下一步计划：

- 人工检查 baseline_evaluated.jsonl；
- 记录错误类型；
- 编写第一版 reports/baseline_analysis.md；
- 后续改进 evaluator。

---
## Day9

今天完成了 Baseline 第一轮测试，使用 `Qwen/Qwen2.5-1.5B-Instruct` 对 10 道基础数学题进行直接解答，并将结果保存到 `results/baseline_results.jsonl`。

初版 evaluator 使用简单字符串匹配，自动评测准确率为 80%。人工检查后发现，主要误判来自数学等价答案的不同表达方式，例如多解方程格式不同、分数和小数表达不同。

下一步计划是增强 evaluator，使其支持简单数值等价判断，并继续整理 Baseline 实验分析报告。

---

## Day 10

完成内容：

- 改进 `src/evaluator.py`；
- 保留简单字符串匹配；
- 新增数值抽取函数 `extract_numeric_values()`；
- 新增数值等价判断函数 `contains_numeric_answers()`；
- 解决 `3/5` 与 `0.6` 的等价判断问题；
- 解决 `x=2 或 x=3` 与 `x1=2, x2=3` 的格式差异问题；
- 重新评测 Baseline 结果；
- 更新 `reports/baseline_analysis.md`。

当前理解：

- 数学答案不能只依赖字符串匹配；
- 同一个数学答案可能有多种表达形式；
- 分数、小数、方程解顺序变化都会导致简单匹配误判；
- evaluator 本身也是数学推理系统的重要组成部分；
- 后续可以进一步引入 SymPy 进行表达式等价判断。

下一步计划：

- 初步引入 SymPy；
- 编写 `src/sympy_checker.py`；
- 测试方程求解、表达式化简、导数和积分。

---

## Day11

今天使用 Day10 改进后的 evaluator 对 Day9 的 Baseline 结果进行了重新评测。
运行命令：

```bash
python -m src.evaluator
```

评测结果：

```text
Evaluated 10 results.
Correct: 10
Accuracy: 100.00%
Saved evaluated results to results/baseline_evaluated.jsonl
```

随后检查了 `results/baseline_evaluated.jsonl` 文件，确认 10 道题的自动判定结果均为正确。
本次结果说明，增强后的 evaluator 已经能够处理当前测试集中出现的简单数学等价表达问题，例如多解方程格式差异、分数和小数等价。
需要注意的是，当前测试集只有 10 道基础题，结果不能代表模型在复杂数学推理任务上的稳定表现。后续需要扩展测试集，并继续增强 evaluator 的答案类型判断能力。

## Day12

今天整理了 Baseline 阶段的运行流程，确认 `baseline_solver` 和 `evaluator` 都可以正常运行。
当前 Baseline 流程为：

```text
data/test_questions.jsonl
↓
python -m src.baseline_solver
↓
results/baseline_results.jsonl
↓
python -m src.evaluator
↓
results/baseline_evaluated.jsonl
```

同时检查并更新了 README 中的运行命令，使文档中的命令与实际项目运行方式保持一致。
当前 Baseline 阶段已经完成最小闭环，下一步计划是进入 RAG 阶段，开始准备数学知识库内容。
