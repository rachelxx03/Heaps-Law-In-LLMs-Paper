import json
from transformers import GPT2Tokenizer
import pickle

# Load the pickle file
def load_pickle(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

# Decode the GPT-2 tokens with a specified interval
def decode_gpt2_tokens(encoded_tokens_list, slice_interval):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    decoded_texts = [tokenizer.decode(tokens[slice_interval]) for tokens in encoded_tokens_list]
    return decoded_texts

# Save the decoded texts to a JSON file
def save_to_json(decoded_texts, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(decoded_texts, json_file, ensure_ascii=False, indent=4)

# Example usage
pickle_file_path = 'generatedData/few_shot_pubmed.pickle'
output_json_file_path = 'data/rawdata/few_shot_pubmed_decoded_texts.json'

data = load_pickle(pickle_file_path)

# Specify the slice interval, e.g., [70:] (from index 70 to the end)
slice_interval = slice(850, None)

decoded_texts = decode_gpt2_tokens(data, slice_interval)
save_to_json(decoded_texts, output_json_file_path)

print(f'Decoded texts have been saved to {output_json_file_path}')
