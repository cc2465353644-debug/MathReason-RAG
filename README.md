# MathReason-RAG：面向数学推理的大模型检索增强与自验证系统

## 1. 项目简介

MathReason-RAG 是一个面向数学推理任务的轻量级 AI 系统。

用户输入一道数学题后，系统会调用本地小模型或 API 模型进行解题，并结合 RAG 检索相关数学知识点、公式和例题，引导模型进行分步骤推理。同时，系统会使用 SymPy 对部分数学计算过程进行验证，尝试发现计算错误并进行修正。

本项目的目标不是训练一个新的大模型，而是构建一个完整的数学推理增强系统，用于探索：

- RAG 是否能提升数学题解答效果；
- CoT 分步骤推理是否能提高答案可解释性；
- SymPy 是否能辅助验证数学计算；
- 不同解题方法在准确率上的差异；
- 模型在数学推理任务中的常见错误类型。

---

## 2. 项目目标

本项目最终计划实现以下功能：

1. 用户输入一道数学题；
2. 系统调用本地模型或 API 模型生成答案；
3. 系统检索相关知识点、公式和例题；
4. 使用 CoT Prompt 引导模型分步骤推理；
5. 使用 SymPy 检查部分计算是否正确；
6. 对比 Baseline、RAG、CoT、RAG + CoT + SymPy 等方法；
7. 输出准确率统计和错误分析报告；
8. 提供命令行或网页 Demo；
9. 形成 GitHub 仓库、技术报告和复试展示材料。

---

## 3. 当前开发阶段

当前项目处于第一阶段：Baseline 系统搭建。

本阶段目标是先完成一个最小可运行闭环：

```text
数学题数据
↓
调用模型解题
↓
保存模型输出
↓
判断答案正确性
↓
生成初步分析报告
```
当前优先完成：

 - 搭建项目目录结构

 - 编写本地模型测试脚本

 - 准备第一批数学测试题

 - 实现 Baseline 解题流程

 - 保存模型输出结果

 - 初步实现答案评测

 - 编写第一版实验分析

## 4. 系统架构设计
计划中的系统整体流程如下：
```test
用户输入数学题
        ↓
题目预处理
        ↓
RAG 检索相关知识点、公式和例题
        ↓
构造 Prompt
        ↓
调用大模型生成分步骤解答
        ↓
SymPy 检查关键计算
        ↓
发现错误后尝试自我修正
        ↓
输出最终答案、推理过程和错误分析
```
系统主要模块包括：

| 模块 | 作用 |
|---|---|
| Model Client	| 调用本地模型或 API 模型 |
| Prompt Builder | 构造不同类型的 Prompt |
| Retriever| 检索数学知识库 |
| Solver| 控制不同解题流程|
| SymPy Checker| 检查数学计算是否正确|
| Evaluator| 判断模型答案是否正确|
| Metrics| 统计准确率和错误类型|
| UI / CLI|	提供网页或命令行交互界面|
## 5. 项目目录结构
```test
MathReason-RAG/
├── README.md
├── requirements.txt
├── main.py
├── app.py
├── src/
│   ├── model_client.py
│   ├── prompts.py
│   ├── baseline_solver.py
│   ├── rag_solver.py
│   ├── cot_solver.py
│   ├── self_verify_solver.py
│   ├── sympy_checker.py
│   ├── evaluator.py
│   └── metrics.py
├── rag/
│   ├── build_chunks.py
│   ├── build_index.py
│   └── retriever.py
├── data/
│   ├── test_questions.jsonl
│   └── knowledge_base/
├── results/
│   ├── baseline_results.jsonl
│   ├── rag_results.jsonl
│   ├── cot_results.jsonl
│   └── self_verify_results.jsonl
├── reports/
│   ├── baseline_analysis.md
│   ├── rag_analysis.md
│   ├── error_analysis.md
│   ├── case_studies.md
│   └── figures/
├── docs/
│   ├── dev_log.md
│   ├── system_design.md
│   └── technical_report.md
└── presentation/
    ├── demo_script.md
    └── slides.pptx
```
## 6. 环境要求
当前计划使用的主要环境如下：
```test
Python >= 3.10
PyTorch
Transformers
Sentence-Transformers
FAISS / Chroma
SymPy
Pandas
Matplotlib
Streamlit
```
本项目计划优先支持本地轻量模型推理，例如：
```test
Qwen/Qwen2.5-1.5B-Instruct
```
也会预留 API 模型接口，用于后续对比实验。

## 7. 安装方法
创建虚拟环境：
```bash
conda create -n mathreason python=3.10
conda activate mathreason
```
安装依赖：
```bash
pip install -r requirements.txt
```
如果还没有 `requirements.txt`，可以先手动安装基础依赖：
```bash
pip install torch transformers accelerate sympy pandas matplotlib streamlit
```
后续 RAG 阶段再安装：
```bash
pip install sentence-transformers faiss-cpu
```
## 8. 快速开始
### 8.1 测试本地模型生成
```bash
python tests/test_generation.py
```
预期效果：
```test
输入一道数学题，模型输出解题过程和最终答案。
```
### 8.2 测试 SymPy 数学计算
```bash
python tests/test_sympy.py
```
预期效果：
```test
SymPy 能够求解方程、求导、积分或化简表达式。
```
### 8.3 运行 Baseline 解题流程
运行 Baseline 解题脚本：
```bash
python -m src.baseline_solver
```
预期效果：
```test
读取 data/test_questions.jsonl 中的数学题，
调用模型生成答案，
并将结果保存到 results/baseline_results.jsonl。
```
运行 evaluator 自动评测：
```bash
python -m src.evaluator
```
预期效果：
```test
读取 results/baseline_results.jsonl，
对模型答案进行自动评测，
并将评测结果保存到 results/baseline_evaluated.jsonl。
```
如果需要一键运行完整 Baseline 流程，可以使用：
```bash
python run_baseline.py
```
预期效果：
```test
依次运行 Baseline 解题和 evaluator 自动评测，
生成 baseline_results.jsonl 和 baseline_evaluated.jsonl。
```
## 9. 数据格式说明
### 9.1 测试题数据格式
测试题存放在：
```test
data/test_questions.jsonl
```
每一行是一道题，例如：
```json
{"id": "algebra_001", "question": "解方程：x^2 - 5x + 6 = 0", "answer": "x=2 或 x=3", "topic": "代数", "difficulty": "easy"}
```
字段说明：

字段|	含义
|---|---|
id|	题目编号
question|	题目内容
answer|	标准答案
topic|	知识点类别
difficulty|	难度等级
### 9.2 模型输出结果格式
模型结果计划保存到：
```test
results/baseline_results.jsonl
```
示例：
```json
{
  "id": "algebra_001",
  "question": "解方程：x^2 - 5x + 6 = 0",
  "standard_answer": "x=2 或 x=3",
  "model_answer": "由因式分解可得 (x-2)(x-3)=0，所以 x=2 或 x=3。",
  "is_correct": true
}
```
## 10. 实验设计
本项目计划对比以下几种方法：

方法|	RAG|	CoT|	SymPy|	说明
|---|---|---|---|---|
Baseline|	否|	否|	否|	模型直接解题
RAG|	是|	否|	否|	检索知识后解题
CoT|	否|	是|	否|	引导模型分步骤推理
RAG + CoT|	是|	是|	否|	检索增强 + 分步骤推理
RAG + CoT + SymPy|	是|	是|	是|	完整自验证流程

主要评测指标：

 - 答案准确率；

 - 可解析率；

 - SymPy 校验通过率；

 - 错误类型分布；

 - 不同方法之间的准确率提升。

## 11. 错误分析方向
本项目会对模型错误进行分类，包括：

错误类型|	说明
|---|---|
知识点错误|	使用了错误公式或错误定理
计算错误|	代数计算、求导、积分等步骤出错
推理跳步|	中间步骤缺失，导致结论不可靠
题意理解错误|	没有正确理解题目要求
答案格式错误|	答案正确但格式无法自动识别
检索干扰|	RAG 检索到无关内容，影响模型判断
## 12. 开发计划
当前开发计划分为以下阶段：

阶段|	目标
|---|---|
阶段一|	完成 Baseline 解题系统
阶段二|	构建数学知识库和 RAG 检索模块
阶段三|	加入 CoT 分步骤推理
阶段四|	加入 SymPy 数学验证
阶段五|	实现自验证和自动纠错
阶段六|	完成实验评测和错误分析
阶段七|	开发命令行或网页 Demo
阶段八|	整理技术报告和展示材料
## 13. 当前 TODO
近期优先任务：

 - 编写 `tests/test_generation.py`

 - 编写 `tests/test_sympy.py`

 - 准备 10 道基础数学题

 - 编写 `data/test_questions.jsonl`

 - 实现 `src/baseline_solver.py`

 - 保存模型输出到 `results/baseline_results.jsonl`

 - 编写 `docs/dev_log.md`

 - 完成第一版 `reports/baseline_analysis.md`

## 14. 项目特色
本项目的特点包括：

1. 不依赖大规模模型训练；

2. 适合个人电脑本地实验；

3. 结合数学专业背景；

4. 覆盖 RAG、Prompt Engineering、CoT、工具调用和评测；

5. 强调可解释推理和错误分析；

6. 适合作为 AI 项目作品集和复试展示项目。

## 15. 后续改进方向
未来可以继续扩展：

 - 支持更多数学题型；

 - 引入更强的 API 模型；

 - 加入本地 7B 量化模型对比；

 - 改进答案自动判定逻辑；

 - 增强 SymPy 对复杂步骤的解析能力；

 - 加入更完整的 Agent 工具调用流程；

 - 提供更美观的 Streamlit Web Demo；

 - 扩展到高中数学、大学数学或竞赛数学场景。

## 16. 项目状态
当前状态：
```test
开发中
```
当前版本：
```test
v0.1.0
```
当前重点：
```test
完成 Baseline 解题系统和第一批测试题评测。
```
