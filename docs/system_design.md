# System Design

## 1. 项目目标

MathReason-RAG 的目标是构建一个面向数学推理任务的检索增强与自验证系统。

用户输入一道数学题后，系统会调用大模型生成解答，并在后续版本中结合 RAG 检索、CoT 分步骤推理和 SymPy 数学验证，提高数学推理过程的可解释性和可靠性。

---

## 2. 当前阶段：Baseline 系统

当前阶段先实现最基础的 Baseline 解题流程。

Baseline 不使用 RAG、不使用 SymPy 自验证，只测试模型直接解题的效果。

流程如下：

```text
读取数学题
    ↓
构造基础 Prompt
    ↓
调用本地模型生成答案
    ↓
保存模型输出
    ↓
人工或程序判断答案
    ↓
生成初步分析报告
```

---

## 3. 最终系统流程

最终系统计划如下：

```text
用户输入数学题
    ↓
题目预处理
    ↓
RAG 检索相关知识点、公式和例题
    ↓
构造 CoT Prompt
    ↓
调用大模型分步骤解题
    ↓
提取关键计算步骤
    ↓
使用 SymPy 校验
    ↓
发现错误后重新提示模型修正
    ↓
输出最终答案、推理过程和错误分析
```

---

## 4. 核心模块设计

| 模块 | 文件 | 作用 |
|---|---|---|
| Model Client | `src/model_client.py` | 统一管理本地模型或 API 模型调用 |
| Prompt Builder | `src/prompts.py` | 构造不同解题模式的 Prompt |
| Baseline Solver | `src/baseline_solver.py` | 实现模型直接解题 |
| Evaluator | `src/evaluator.py` | 判断模型答案是否正确 |
| SymPy Checker | `src/sympy_checker.py` | 校验方程、化简、求导、积分等计算 |
| Retriever | `rag/retriever.py` | 根据题目检索相关数学知识 |
| Metrics | `src/metrics.py` | 统计准确率和错误类型 |
| CLI | `main.py` | 命令行入口 |
| Web App | `app.py` | Streamlit 网页入口 |

---

## 5. 数据文件设计

### 5.1 测试题文件

测试题保存到：

```text
data/test_questions.jsonl
```

示例：

```json
{"id": "algebra_001", "question": "解方程：x^2 - 5x + 6 = 0", "answer": "x=2 或 x=3", "topic": "代数", "difficulty": "easy"}
```

---

### 5.2 模型输出文件

Baseline 结果保存到：

```text
results/baseline_results.jsonl
```

示例：

```json
{"id": "algebra_001", "question": "解方程：x^2 - 5x + 6 = 0", "standard_answer": "x=2 或 x=3", "model_answer": "由因式分解可得...", "is_correct": true}
```

---

## 6. 实验对比设计

后续计划对比以下方法：

| 方法 | RAG | CoT | SymPy | 说明 |
|---|---|---|---|---|
| Baseline | 否 | 否 | 否 | 模型直接回答 |
| RAG | 是 | 否 | 否 | 检索相关知识后回答 |
| CoT | 否 | 是 | 否 | 分步骤推理 |
| RAG + CoT | 是 | 是 | 否 | 检索增强 + 分步骤推理 |
| RAG + CoT + SymPy | 是 | 是 | 是 | 完整自验证系统 |

---

## 7. 当前优先级

当前阶段只关注：

1. 准备第一批数学题；
2. 调用模型批量解题；
3. 保存模型输出；
4. 初步判断答案；
5. 写 Baseline 分析报告。

暂时不做：

- RAG；
- 微调；
- Agent；
- 网页美化；
- 复杂自动判题。
