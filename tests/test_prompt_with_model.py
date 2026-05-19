from src.model_client import LocalModelClient
from src.prompts import build_basic_prompt, build_cot_prompt


def main():
    question = "解方程：x^2 - 5x + 6 = 0"

    client = LocalModelClient()

    print("===== Basic Prompt Result =====")
    basic_prompt = build_basic_prompt(question)
    basic_answer = client.generate(basic_prompt)
    print(basic_answer)

    print("\n===== CoT Prompt Result =====")
    cot_prompt = build_cot_prompt(question)
    cot_answer = client.generate(cot_prompt)
    print(cot_answer)


if __name__ == "__main__":
    main()
