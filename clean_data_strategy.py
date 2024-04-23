import re
import unicodedata


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
        return data.split()

class CleanData:
    def __init__(self, strategy: DataProcessing = None):
        self._strategy = strategy

    def set_strategy(self, strategy: DataProcessing):
        self._strategy = strategy

    def do_something(self, data: str):
        if self._strategy:
            return self._strategy.process(data)
        else:
            raise Exception('DataProcessing strategy not set')

data = "Hello! This is an example sentence. (With some punctuation...)"
cleaner = CleanData(SimpleProcessing())
clean_data = cleaner.do_something(data)
print(clean_data)

