from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-1.5B-Instruct",
    device="cuda"
)

prompt = """
你是一个数学解题助手。
请解答下面这道数学题，并给出必要的解题过程。

题目：解方程 x^2 - 5x + 6 = 0
"""

result = pipe(prompt, max_new_tokens=200)

print(result[0]["generated_text"])

