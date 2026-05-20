from src.evaluator import (
    simple_match,
    extract_numeric_values,
    contains_numeric_answers,
)


def main():
    test_cases = [
        {
            "standard": "x=2 或 x=3",
            "model": "所以方程的两个解为 x1=2, x2=3。",
            "expected": True,
        },
        {
            "standard": "3/5",
            "model": "取到红球的概率为 0.6。",
            "expected": True,
        },
        {
            "standard": "x=4",
            "model": "最终答案是 x=4。",
            "expected": True,
        },
        {
            "standard": "x=4",
            "model": "最终答案是 x=5。",
            "expected": False,
        },
    ]

    for case in test_cases:
        standard = case["standard"]
        model = case["model"]
        expected = case["expected"]

        string_result = simple_match(standard, model)
        numeric_result = contains_numeric_answers(standard, model)
        final_result = string_result or numeric_result

        print("=" * 60)
        print("Standard:", standard)
        print("Model:", model)
        print("Standard numbers:", extract_numeric_values(standard))
        print("Model numbers:", extract_numeric_values(model))
        print("String match:", string_result)
        print("Numeric match:", numeric_result)
        print("Final result:", final_result)
        print("Expected:", expected)


if __name__ == "__main__":
    main()
