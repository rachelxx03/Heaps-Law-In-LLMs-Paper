import argparse
import json
import random
from transformers import GPT2Tokenizer
from abc import ABC, abstractmethod
import os

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Function to choose randomly from the data
def select_random_elements(array, k):
    if len(array) < k:
        return "Array does not contain enough elements"
    return random.sample(array, k)

class PromptStrategy(ABC):
    @abstractmethod
    def generate_prompt_single(self, prompt, example, command, length):
        pass

    @abstractmethod
    def generate_prompt_array(self, prompt, example, command, length):
        pass

    def save_prompt(self, prompt, file_name):
        # Ensure the directory exists
        os.makedirs("prompt", exist_ok=True)

        with open(f"prompt/{file_name}", 'w') as file:
            json.dump(prompt, file, indent=4)

        return f"Prompt saved to {file_name}"

class ZeroShot(PromptStrategy):
    def generate_prompt_single(self, prompt, example, command, length):
        givenPrompt = command + prompt[:length]
        return givenPrompt

    def generate_prompt_array(self, prompt, example, command, length):
        prompts = []
        for i in prompt:
            token_ids = tokenizer.encode(" ".join(i.split()[:100]))
            prompt_text = tokenizer.decode(token_ids[:length])
            givenPrompt = command + " " + prompt_text
            prompts.append(givenPrompt)
        return prompts

class OneShot(PromptStrategy):
    def generate_prompt_single(self, prompt, example, command, length):
        return 0

    def generate_prompt_array(self, prompt, example, command, length):
        prompts = []
        for i in prompt:
            random_item = random.choice(example)
            random_item = tokenizer.encode(" ".join(random_item.split()[:150]))
            random_item = tokenizer.decode(random_item[:150])

            examplePrompt = command + " " + random_item + " "
            token_ids = tokenizer.encode(" ".join(i.split()[:100]))
            prompt_text = tokenizer.decode(token_ids[:length])
            givenPrompt = examplePrompt + command + " " + prompt_text
            prompts.append(givenPrompt)
        return prompts

class FewShot(PromptStrategy):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    def generate_prompt_single(self, prompt, example, command, length):
        return 0

    def generate_prompt_array(self, prompt, example, command, length):
        def generate_example_prompts(example, num_examples=5):
            example_prompts = []
            for _ in range(num_examples):
                random_item = random.choice(example)
                encoded_item = self.tokenizer.encode(random_item, truncation=True, max_length=150)
                example_prompt = command + " " + self.tokenizer.decode(encoded_item)
                example_prompts.append(example_prompt)
            return " ".join(example_prompts)

        def generate_prompt_text(i):
            token_ids = self.tokenizer.encode(i, truncation=True, max_length=100)
            return self.tokenizer.decode(token_ids[:length])

        prompts = []
        for i in prompt:
            example_prompts = generate_example_prompts(example)
            prompt_text = generate_prompt_text(i)
            given_prompt = example_prompts + " " + command + " " + prompt_text
            prompts.append(given_prompt)
        return prompts
class PromptContext:
    def __init__(self, strategy: PromptStrategy):
        self.strategy = strategy

    def generate_prompt_single(self, prompt, example, command, length):
        return self.strategy.generate_prompt_single(prompt, example, command, length)

    def generate_prompt_array(self, prompt, example, command, length):
        return self.strategy.generate_prompt_array(prompt, example, command, length)

    def save_strategy_output(self, prompt, file_name):
        return self.strategy.save_prompt(prompt, file_name)

def LoadData(file_path):
    with open(file_path, 'r') as file:
        texts = json.load(file)
    return texts

def generate_all_prompt(example, prompt, name, command, length):
    promptStra = [ZeroShot(), OneShot(), FewShot()]
    namePrompt = ["zero_shot_", "one_shot_", "few_shot_"]

    for i in range(len(promptStra)):
        promtS = PromptContext(strategy=promptStra[i])
        arr = promtS.generate_prompt_array(prompt, example, command, length)
        promtS.save_strategy_output(arr, namePrompt[i] + name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--datasourse', type=int, default="0", help='choose where is the source of data')
    parser.add_argument('--name', type=str, help='choose name for the output file')
    parser.add_argument('--prompt', type=str)

    args = parser.parse_args()

    example = LoadData("data/selectedData/400_remaining_50000_PubMed.json")
    prompt = LoadData("data/selectedData/400_subset_10000_PubMed.json")

    generate_all_prompt(example, prompt, args.name, args.prompt, 50)
