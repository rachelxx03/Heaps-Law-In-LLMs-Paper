import argparse
import json
import re

import pandas as pd
import unicodedata
import pickle
from datasets import load_dataset
from spellchecker import SpellChecker
import contractions
from nltk.corpus import wordnet as wn
import tqdm
from concurrent.futures import ThreadPoolExecutor


# Ensure WordNet corpus is loaded before threading
wn.ensure_loaded()

class DataProcessing:
    def process(self, data: str):
        pass

class OpenVocab(DataProcessing):
    def process(self, data: str):
        return self.split_by_space(
               self.expand_contractions(
               self.correct_spelling(
               self.remove_punctuation(
               self.remove_non_ascii(
               self.lower_case(data))))))

    def lower_case(self, data: str):
        return data.lower()

    def remove_non_ascii(self, data: str):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, data: str):
        return re.sub(r'[^\w\s]', '', data).strip()

    def correct_spelling(self, text: str):
        spell = SpellChecker()
        misspelled = spell.unknown(text.split())
        corrected_text = text.split()

        for idx, word in enumerate(corrected_text):
            if word in misspelled:
                corrected_word = spell.correction(word)
                if corrected_word is None:
                    corrected_word = word
                corrected_text[idx] = corrected_word

        return ' '.join(corrected_text)

    def expand_contractions(self, text: str):
        return contractions.fix(text)

    def split_by_space(self, data: str):
        return data.split()

class CloseVocab(DataProcessing):
    def process(self, data: str):
        return self.filter_words_in_vocab_database(
               self.split_by_space(
               self.expand_contractions(
               self.correct_spelling(
               self.remove_punctuation(
               self.remove_non_ascii(
               self.lower_case(data)))))))

    def lower_case(self, data: str):
        return data.lower()

    def remove_non_ascii(self, data: str):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, data: str):
        return re.sub(r'[^\w\s]', '', data).strip()

    def correct_spelling(self, text):
        spell = SpellChecker()
        misspelled = spell.unknown(text.split())
        corrected_text = text.split()

        for idx, word in enumerate(corrected_text):
            if word in misspelled:
                corrected_word = spell.correction(word)
                if corrected_word is None:
                    corrected_word = word
                corrected_text[idx] = corrected_word

        return ' '.join(corrected_text)

    def filter_words_in_vocab_database(self, words):
        return [word for word in words if len(wn.synsets(word)) > 0]

    def expand_contractions(self, text):
        return contractions.fix(text)

    def split_by_space(self, data: str):
        return data.split()

class SimpleProcessing(DataProcessing):
    def process(self, data: str):
        return self.split_by_space(
               self.remove_punctuation(
               self.remove_non_ascii(
               self.lower_case(data))))

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
        with ThreadPoolExecutor() as executor:
            results = list(tqdm.tqdm(executor.map(self.clean, data), total=len(data)))
        return results

    def saveData(self, data: str, name: str):
        file_path = f'data/cleandata/{name}.json'
        with open(file_path, 'w') as file:
            json.dump(data, file)
        print(f"data have been saved to {file_path} successfully")

def loadData(type):
    if type == 1 :
        my_dataset = load_dataset(args.inputdata)
        df = pd.DataFrame(my_dataset['train'])
        return df[args.choosedata][0:10000]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--datasourse', type=int, default="0", help='choose where is the sourse of data')
    parser.add_argument('--inputdata', type=str, help='what is the name of the data')
    parser.add_argument('--choosedata', type=str, help='what is the name of the column?')
    parser.add_argument('--name', type=str, help='choose name for the outputfile')
    args = parser.parse_args()

    data = loadData(args.datasourse)
    cleaner = CleanData(SimpleProcessing())
    clean_data = cleaner.cleanTheArray(data)
    cleaner.saveData(clean_data,args.name)



