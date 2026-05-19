from src.model_client import LocalModelClient


def main():
    client = LocalModelClient()

    prompt = """
请你解下面这道数学题，并给出清晰步骤。

题目：解方程：x^2 - 5x + 6 = 0
"""

    answer = client.generate(prompt)

    print(answer)


if __name__ == "__main__":
    main()
