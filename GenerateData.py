import pickle
import torch
import json
from torch.utils.data import Dataset, DataLoader
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

class VarrianDataset(Dataset):
    def __init__(self, input_ids):
        self.input_ids = input_ids

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx]

class LLMsGeneration:
    def __init__(self, model, tokenizer, device, start_point, end_point):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.startPoint = start_point
        self.endPoint = end_point
        self.rawDoc = None

    def loadArray(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)[self.startPoint:self.endPoint]

        prompts = [item["prompt"] for item in data]

        all_input_ids = self.tokenizer(prompts, return_tensors="pt", truncation=True, padding="max_length", max_length=50).input_ids
        all_input_ids = all_input_ids.to(self.device)

        dataset = VarrianDataset(all_input_ids)
        dataloader = DataLoader(dataset, batch_size=32, shuffle=False)

        outputs = []
        max_position_embeddings = self.model.config.max_position_embeddings

        for batch_input_ids in dataloader:
            if batch_input_ids.shape[1] > 50:
                raise ValueError(f"Input IDs length ({batch_input_ids.shape[1]}) exceeds the specified input length (50 tokens).")

            total_length = 50 + 300

            if total_length > max_position_embeddings:
                print(f"Warning: Desired total length ({total_length}) exceeds model's max position embeddings ({max_position_embeddings}). Truncating to {max_position_embeddings}.")
                total_length = max_position_embeddings

            generated = self.model.generate(batch_input_ids,
                                            max_length=total_length,
                                            pad_token_id=self.tokenizer.pad_token_id)

            outputs.extend(generated.cpu().numpy())

        self.rawDoc = outputs

    def decode(self, data):
        return self.tokenizer.decode(data, skip_special_tokens=True)

if __name__ == '__main__':
    # Set up start and end points, model, tokenizer, and device
    start_point = 0  # Replace with actual start point
    end_point = 10  # Replace with actual end point
    output_pickle_file = 'output.pickle'  # Replace with actual output file path
    model_name = 'EleutherAI/gpt-neo-1.3B'
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Initialize model and tokenizer
    model = GPTNeoForCausalLM.from_pretrained(model_name).to(device)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    # Set padding token
    tokenizer.pad_token = tokenizer.eos_token

    # Initialize LLMsGeneration instance
    llms_generation = LLMsGeneration(model, tokenizer, device, start_point, end_point)

    # Load array and generate text
    llms_generation.loadArray('prompt/few_shot_PubMed.json')

    # Save the generated text
    with open(output_pickle_file, 'wb') as file:
        pickle.dump(llms_generation.rawDoc, file)
