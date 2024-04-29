from transformers import AutoModelForCausalLM, AutoTokenizer

import loadData


class TextGenerator:
    def __init__(self, model_name):
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def generate_text(self, prompt, max_length=1024, temperature=0.9):
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids

        gen_tokens = self.model.generate(
            input_ids,
            do_sample=True,
            temperature=temperature,
            max_length=max_length,
            eos_token_id=self.tokenizer.eos_token_id
        )

        return self.tokenizer.batch_decode(gen_tokens)[0]

class TextGeneratorFactory:
    @staticmethod
    def create_text_generator(model_name):
        return TextGenerator(model_name)

# Usage example:
if __name__ == "__main__":
    # Create a text generator for GPT-2
    gpt2_generator = TextGeneratorFactory.create_text_generator("gpt2")
    prompt = "GPT2 is a model developed by OpenAI."
    print(gpt2_generator.generate_text(prompt))
    loadData.DataLoader
    # Create a text generator for another model, e.g., GPT-Neo
    gpt_neo_generator = TextGeneratorFactory.create_text_generator("EleutherAI/gpt-neo-2.7B")
    another_prompt = "GPT-Neo is another model developed by EleutherAI."
    print(gpt_neo_generator.generate_text(another_prompt))
