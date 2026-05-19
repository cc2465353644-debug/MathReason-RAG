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

完成内容：

- 实现 `src/model_client.py`；
- 使用 `LocalModelClient` 封装本地模型调用；
- 成功调用 `Qwen/Qwen2.5-1.5B-Instruct`；
- 输入一道一元二次方程测试题，模型能够输出正确解答。

测试命令：

```bash
python src/model_client.py
```

测试题目：
```test
解方程：x^2 - 5x + 6 = 0
```

测试结果：
```test
模型能够给出 x=2 或 x=3，结果正确。
```

当前理解：

- model_client.py 是模型调用中心；
- 后续 Baseline、RAG、CoT 都会复用这个模块；
- 测试文件的作用是验证模块是否被改坏；
- 当前模型调用已经从临时 demo 进入可复用模块阶段。

下一步计划：

- 编写 src/prompts.py；
- 将 Prompt 模板从模型调用代码中拆出来；
- 为后续 Baseline 批量解题做准备。

为了更好进行调试，建立新的文件：

src/ 下面的文件 = 正式功能代码
tests/ 下面的文件 = 用来验证功能是否正常

测试命令：

```bash
python tests/test_model_client.py
```

测试题目：
```test
解方程：x^2 - 5x + 6 = 0
```

测试现象：

- 程序可以正常加载模型；
- 模型可以生成答案；
- 但生成的数学答案不完全正确。

初步原因分析：

- 当前使用的是轻量级本地模型 Qwen/Qwen2.5-1.5B-Instruct；
- 小模型在数学推理任务上存在不稳定性；
- 当前 Prompt 较简单；
- 当前生成参数存在随机性。

后续改进方向：

- 使用更稳定的生成参数，例如 do_sample=False；
- 设计更清晰的数学解题 Prompt；
- 后续使用 SymPy 对计算结果进行校验；
- 在 Baseline 阶段记录模型错误，为后续 RAG 和自验证提供对比。

在 src/ 下面放一个空文件：

```test
src/__init__.py
```

它的作用就是告诉 Python：

```test
src 不是普通文件夹，而是一个 Python 包。
```

同理，在 tests/ 下面放：

```test
tests/__init__.py
```

是为了可以用这种方式运行测试：

```bash
python -m tests.test_model_client
```

---

## Day 5

完成内容：

- 编写 `src/prompts.py`；
- 实现 Basic Prompt、CoT Prompt 和 Answer Only Prompt；
- 编写 `tests/test_prompts.py` 测试 Prompt 模板生成；
- 编写 `tests/test_prompt_with_model.py`，初步观察不同 Prompt 对模型输出的影响。

测试命令：

```bash
python src/prompts.py
python -m tests.test_prompts
python -m tests.test_prompt_with_model
```

当前理解：

- model_client.py 负责模型调用；
- prompts.py 负责提示词管理；
- 将 Prompt 单独拆出来，可以避免后续代码混乱；
- CoT Prompt 的作用是引导模型输出更完整的推理步骤；
- Prompt 会影响模型回答的结构，但不能保证答案一定正确。

遇到的问题：

- 小模型在数学题上的回答仍可能不稳定；
- 后续需要通过批量测试、SymPy 校验和错误分析来系统评估。
- 下一步计划：
- 准备第一批数学测试题；
- 创建 data/test_questions.jsonl；
- 为 Baseline 批量解题做准备。

测试题目：

```text
解方程：x^2 - 5x + 6 = 0
```

观察结果：

- Basic Prompt 能够引导模型使用求根公式解题；
- CoT Prompt 能够引导模型按照知识点、方法、推理、检查、答案的结构输出；
- 当前输出中包含了原始 Prompt，原因是 tokenizer.decode(outputs[0]) 会同时解码输入和生成内容；
- Basic Prompt 的输出被截断，说明 max_new_tokens=300 对数学推理可能偏短。

改进计划：

- 修改 model_client.py，只返回模型新生成的内容；
- 将默认 max_new_tokens 调整为 512；
- 数学题生成时优先使用 do_sample=False，减少随机性。