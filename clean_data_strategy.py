import re
import unicodedata
import pickle


class DataProcessing:
    def process(self, data: str):
        pass

class SimpleProcessing(DataProcessing):
    def process(self, data: str):
        return self.split_by_space(self.remove_punctuation(self.remove_non_ascii(self.lower_case(data))))

    def lower_case(self, data: str):
        return data.lower()

    def remove_non_ascii(self, data: str):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, data: str):
        return re.sub(r'[^\w\s]', '', data).strip()

    def split_by_space(self, data: str):
        return data.split(" ")

class CleanData:
    def __init__(self, strategy: DataProcessing = None):
        self._strategy = strategy

    def set_strategy(self, strategy: DataProcessing):
        self._strategy = strategy

    def clean(self, data: str):
        if self._strategy:
            return self._strategy.process(data)
        else:
            raise Exception('DataProcessing strategy not set')
    def cleanTheArray(self, data):
        return [self.clean(i) for i in data ]

    def saveData(self, data: str, name: str ):
        file_path = f'data/cleandata/{name}.pickle'
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
        print(f"data have been saved to {file_path} sucessfully")
if __name__ == "__main__":
    data = "Hello! This is an example sentence. (With some punctuation...)"
    cleaner = CleanData(SimpleProcessing())
    clean_data = cleaner.clean(data)
    print(clean_data)

