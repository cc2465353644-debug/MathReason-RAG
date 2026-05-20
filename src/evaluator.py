"""
Evaluator module.

This module evaluates whether model answers match standard answers.

Current methods:
1. Simple string matching
2. Numeric equivalence matching
"""

import json
import os
import re
from fractions import Fraction
from typing import Dict, List


def load_jsonl(file_path: str) -> List[Dict]:
    """
    Load data from a JSONL file.
    """

    items = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))

    return items


def save_jsonl(items: List[Dict], output_path: str) -> None:
    """
    Save a list of dictionaries to a JSONL file.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def normalize_text(text: str) -> str:
    """
    Normalize text for simple answer matching.
    """

    text = str(text)
    text = text.lower()
    text = text.replace(" ", "")
    text = text.replace("，", ",")
    text = text.replace("。", ".")
    text = text.replace("：", ":")
    text = text.replace("；", ";")
    text = text.replace("或", "or")
    text = text.replace("和", "and")

    return text


def simple_match(standard_answer: str, model_answer: str) -> bool:
    """
    Check whether the normalized standard answer appears in the model answer.
    """

    standard = normalize_text(standard_answer)
    model = normalize_text(model_answer)

    return standard in model


def extract_numeric_values(text: str) -> List[float]:
    """
    Extract numeric values from text.

    Supports:
    - integers: 5
    - decimals: 0.6
    - fractions: 3/5
    """

    text = str(text)
    values = []

    # Extract fractions first, such as 3/5.
    fraction_pattern = r"[-+]?\d+\s*/\s*[-+]?\d+"
    fractions = re.findall(fraction_pattern, text)

    for frac in fractions:
        try:
            value = float(Fraction(frac.replace(" ", "")))
            values.append(value)
        except ZeroDivisionError:
            continue
        except ValueError:
            continue

    # Remove fractions to avoid extracting numerator and denominator again.
    text_without_fractions = re.sub(fraction_pattern, " ", text)

    # Extract integers and decimals.
    number_pattern = r"[-+]?\d+\.\d+|[-+]?\d+"
    numbers = re.findall(number_pattern, text_without_fractions)

    for num in numbers:
        try:
            values.append(float(num))
        except ValueError:
            continue

    return values


def contains_numeric_answers(
    standard_answer: str,
    model_answer: str,
    tolerance: float = 1e-6
) -> bool:
    """
    Check whether all numeric values in the standard answer appear in the model answer.

    This is a loose matching rule.
    For example:
    - standard: 3/5
    - model: 0.6
    will be considered correct.
    """

    standard_values = extract_numeric_values(standard_answer)
    model_values = extract_numeric_values(model_answer)

    if not standard_values or not model_values:
        return False

    for std_value in standard_values:
        found = False

        for model_value in model_values:
            if abs(std_value - model_value) <= tolerance:
                found = True
                break

        if not found:
            return False

    return True


def evaluate_single_item(item: Dict) -> Dict:
    """
    Evaluate one result item.
    """

    standard_answer = item["standard_answer"]
    model_answer = item["model_answer"]

    if simple_match(standard_answer, model_answer):
        is_correct = True
        evaluation_method = "simple_string_match"
    elif contains_numeric_answers(standard_answer, model_answer):
        is_correct = True
        evaluation_method = "numeric_equivalence_match"
    else:
        is_correct = False
        evaluation_method = "not_matched"

    new_item = dict(item)
    new_item["is_correct"] = is_correct
    new_item["evaluation_method"] = evaluation_method

    return new_item


def evaluate_results(
    input_path: str = "results/baseline_results.jsonl",
    output_path: str = "results/baseline_evaluated.jsonl"
) -> None:
    """
    Evaluate model outputs and save evaluated results.
    """

    results = load_jsonl(input_path)

    evaluated_results = []
    correct_count = 0

    for item in results:
        evaluated_item = evaluate_single_item(item)
        evaluated_results.append(evaluated_item)

        if evaluated_item["is_correct"]:
            correct_count += 1

    total = len(evaluated_results)
    accuracy = correct_count / total if total > 0 else 0

    save_jsonl(evaluated_results, output_path)

    print(f"Evaluated {total} results.")
    print(f"Correct: {correct_count}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Saved evaluated results to {output_path}")


if __name__ == "__main__":
    evaluate_results()
