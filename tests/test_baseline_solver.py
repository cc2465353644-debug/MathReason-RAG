from src.baseline_solver import load_questions


def main():
    questions = load_questions("data/test_questions.jsonl")

    print(f"Loaded {len(questions)} questions.")

    first = questions[0]

    print("First question:")
    print(first)


if __name__ == "__main__":
    main()
