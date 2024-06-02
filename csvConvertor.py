import json
import csv
import os

def combine_json_to_csv(json_folder, output_csv):
    all_data = []

    # Read all JSON files and collect their data
    for json_file in os.listdir(json_folder):
        if json_file.endswith('.json'):
            with open(os.path.join(json_folder, json_file), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                if 'text' in item:
                                    all_data.append(item['text'])
                            elif isinstance(item, str):
                                all_data.append(item)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from {json_file}: {e}")

    # Write the data to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['text'])
        for text in all_data:
            writer.writerow([text])

# Example usage
json_folder = 'data/selectedData'  # Replace with your actual folder path
output_csv = 'data/train.csv'  # Replace with your desired output CSV file path
combine_json_to_csv(json_folder, output_csv)
