import json
import os
from tqdm import tqdm
import pandas as pd
from datasets import load_dataset

class DataLoader:
    def load_data(self):
        pass

class TypeOneLoader(DataLoader):
    def __init__(self, args):
        self.args = args

    def load_data(self):
  # Placeholder for actual import
        my_dataset = load_dataset(self.args.inputdata)
        df = pd.DataFrame(my_dataset['train'])
        data = self.clean_data(df[self.args.choosedata], self.args.name)
        return data

    def clean_data(self, data, name):
        # Assuming a simple cleanup function
        cleaned_data = data.dropna()  # Example cleanup operation
        return cleaned_data

class LocalDataLoader(DataLoader):
    def __init__(self, args):
        self.args = args
    def load_data(self, limit = 7000001):
        start = 0
        _ , file_ext = os.path.splitext(self.args.inputdata)
        if file_ext == '.csv':
            return pd.read_csv(self.args.inputdata)[self.args.choosedata]
        elif file_ext in ['.json', '.jsonl']:  # Support for .jsonl
            data = []
            with open(self.args.inputdata, 'r',  encoding='utf-8') as file:
                for line in tqdm(file):
                    json_data = json.loads(line)  # Parse each line as a JSON object
                    data.append(json_data[self.args.choosedata])  # Extract the desired data
                    start += 1
                    if start == limit:
                        break
            return data
        elif file_ext in ['.xls', '.xlsx']:
            return pd.read_excel(self.args.inputdata)[self.args.choosedata]
        else:
            raise ValueError("Unknown file format")

class DataLoaderFactory:
    def get_loader(self, args):
        if args.datasourse == 1:
            return TypeOneLoader(args)
        elif args.datasourse == 0:
            return LocalDataLoader(args)
        else:
            return DataLoader()

