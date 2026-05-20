import json


def main():
    file_path = "data/test_questions.jsonl"

    questions = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            questions.append(item)

    print(f"Loaded {len(questions)} questions.")

    for q in questions:
        print(q["id"], q["topic"], q["question"], "=>", q["answer"])


if __name__ == "__main__":
    main()
