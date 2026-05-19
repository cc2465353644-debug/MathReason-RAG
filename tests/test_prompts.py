from src.prompts import (
    build_basic_prompt,
    build_cot_prompt,
    build_answer_only_prompt,
)


def main():
    question = "求函数 f(x)=x^2+3x 的导数。"

    basic_prompt = build_basic_prompt(question)
    cot_prompt = build_cot_prompt(question)
    answer_only_prompt = build_answer_only_prompt(question)

    print("===== Basic Prompt =====")
    print(basic_prompt)

    print("\n===== CoT Prompt =====")
    print(cot_prompt)

    print("\n===== Answer Only Prompt =====")
    print(answer_only_prompt)


if __name__ == "__main__":
    main()
