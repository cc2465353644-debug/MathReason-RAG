"""
Model client module.

This module provides a unified interface for calling local language models.
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class LocalModelClient:
    """
    A simple local model client based on Hugging Face Transformers.

    Current default model:
    - Qwen/Qwen2.5-1.5B-Instruct
    """

    def __init__(self, model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading model: {self.model_name}")
        print(f"Using device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        if self.device == "cuda":
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto"
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name
            )
            self.model.to(self.device)

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 512,
        do_sample: bool = False,
        temperature: float = 0.3
    ) -> str:
        """
        Generate text from a prompt.

        Args:
            prompt: The input prompt.
            max_new_tokens: Maximum number of tokens to generate.
            do_sample: Whether to use sampling.
            temperature: Sampling temperature. Only used when do_sample=True.

        Returns:
            The newly generated text.
        """

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        generation_kwargs = {
            "max_new_tokens": max_new_tokens,
            "do_sample": do_sample,
            "pad_token_id": self.tokenizer.eos_token_id
        }

        if do_sample:
            generation_kwargs["temperature"] = temperature

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                **generation_kwargs
            )

        input_length = inputs["input_ids"].shape[1]
        generated_tokens = outputs[0][input_length:]

        result = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return result.strip()


if __name__ == "__main__":
    client = LocalModelClient()

    question = "解方程：x^2 - 5x + 6 = 0"

    prompt = f"""
请你解下面这道数学题，并给出清晰步骤。

题目：{question}
"""

    answer = client.generate(prompt)

    print(answer)
