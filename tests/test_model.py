from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-1.5B-Instruct",
    device="cuda"
)

result = pipe("你好，请解释什么是导数", max_new_tokens=100)

print(result[0]["generated_text"])
