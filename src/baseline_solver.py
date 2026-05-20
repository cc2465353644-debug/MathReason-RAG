"""
Baseline solver.

This module reads math questions from a JSONL file,
uses a local language model to solve them directly,
and saves the model outputs to a JSONL result file.
"""

import json
import os
from typing import List, Dict

from src.model_client import LocalModelClient
from src.prompts import build_basic_prompt


def load_questions(file_path: str) -> List[Dict]:
    """
    Load questions from a JSONL file.

    Args:
        file_path: Path to the question JSONL file.

    Returns:
        A list of question dictionaries.
    """

    questions = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                questions.append(item)

    return questions


def save_result(result: Dict, output_path: str) -> None:
    """
    Save one result item to a JSONL file.

    Args:
        result: A dictionary containing model output and metadata.
        output_path: Path to the output JSONL file.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")


def run_baseline(
    question_path: str = "data/test_questions.jsonl",
    output_path: str = "results/baseline_results.jsonl",
    max_questions: int | None = None
) -> None:
    """
    Run baseline solving.

    Args:
        question_path: Path to the input question file.
        output_path: Path to the output result file.
        max_questions: Maximum number of questions to solve. If None, solve all.
    """

    questions = load_questions(question_path)

    if max_questions is not None:
        questions = questions[:max_questions]

    print(f"Loaded {len(questions)} questions.")

    # Clear old result file before running a new baseline experiment.
    if os.path.exists(output_path):
        os.remove(output_path)

    client = LocalModelClient()

    for index, item in enumerate(questions, start=1):
        question_id = item["id"]
        question = item["question"]
        standard_answer = item["answer"]
        topic = item.get("topic", "")
        difficulty = item.get("difficulty", "")

        print("=" * 80)
        print(f"[{index}/{len(questions)}] Solving question: {question_id}")
        print(f"Question: {question}")

        prompt = build_basic_prompt(question)

        model_answer = client.generate(
            prompt,
            max_new_tokens=512,
            do_sample=False
        )

        result = {
            "id": question_id,
            "question": question,
            "standard_answer": standard_answer,
            "model_answer": model_answer,
            "topic": topic,
            "difficulty": difficulty,
            "method": "baseline"
        }

        save_result(result, output_path)

        print("Model answer:")
        print(model_answer)
        print(f"Saved result to {output_path}")

    print("=" * 80)
    print("Baseline run finished.")


if __name__ == "__main__":
    run_baseline(max_questions=None)
