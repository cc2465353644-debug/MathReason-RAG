"""
Prompt templates for different math solving modes.
"""


def build_basic_prompt(question: str) -> str:
    """
    Build a basic prompt for direct math problem solving.
    """

    prompt = f"""
你是一个数学解题助手。

请解答下面这道数学题，并给出必要的解题过程。

题目：
{question}
"""

    return prompt.strip()


def build_cot_prompt(question: str) -> str:
    """
    Build a Chain-of-Thought style prompt for step-by-step math reasoning.
    """

    prompt = f"""
你是一个严谨的数学解题助手。

请按照以下步骤解答数学题：

1. 判断题目考察的知识点；
2. 写出需要使用的公式或方法；
3. 逐步进行推理和计算；
4. 检查计算过程是否合理；
5. 给出最终答案。

题目：
{question}
"""

    return prompt.strip()


def build_answer_only_prompt(question: str) -> str:
    """
    Build a prompt that asks the model to provide a concise final answer.
    """

    prompt = f"""
请直接给出下面数学题的最终答案，不需要写详细过程。

题目：
{question}

最终答案：
"""

    return prompt.strip()


if __name__ == "__main__":
    test_question = "解方程：x^2 - 5x + 6 = 0"

    print("===== Basic Prompt =====")
    print(build_basic_prompt(test_question))

    print("\n===== CoT Prompt =====")
    print(build_cot_prompt(test_question))

    print("\n===== Answer Only Prompt =====")
    print(build_answer_only_prompt(test_question))
