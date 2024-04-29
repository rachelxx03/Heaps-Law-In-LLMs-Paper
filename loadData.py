import json

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

class JsonLoader(DataLoader):
    def __init__(self, args):
        self.args = args
    def load_data(self):
        with open(self.arg.name, 'r') as file:
            prompts = json.load(file)
        return prompts

class DataLoaderFactory:
    def get_loader(self, type, args):
        if type == 1:
            return TypeOneLoader(args)
        elif type == 0:
            return JsonLoader(args)
        else:
            return DataLoader()

