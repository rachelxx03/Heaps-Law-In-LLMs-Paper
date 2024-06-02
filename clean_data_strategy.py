import re
import time
import unicodedata
import pickle
from spellchecker import SpellChecker
import contractions
from nltk.corpus import wordnet as wn
import tqdm


class DataProcessing:
    def process(self, data: str):
        pass
class OpenVocab(DataProcessing):
    # def process(self, data: str):
    #     return self.split_by_space(
    #            self.expand_contractions(
    #            self.correct_spelling(
    #            self.remove_punctuation(
    #            self.remove_non_ascii(
    #            self.lower_case(data))))))

    def process(self, data: str):
        start_time = time.time()
        data = self.lower_case(data)
        print(f"Time for lower_case: {time.time() - start_time} seconds")

        start_time = time.time()
        data = self.remove_non_ascii(data)
        print(f"Time for remove_non_ascii: {time.time() - start_time} seconds")

        start_time = time.time()
        data = self.remove_punctuation(data)
        print(f"Time for remove_punctuation: {time.time() - start_time} seconds")

        start_time = time.time()
        data = self.correct_spelling(data)
        print(f"Time for correct_spelling: {time.time() - start_time} seconds")

        start_time = time.time()
        data = self.expand_contractions(data)
        print(f"Time for expand_contractions: {time.time() - start_time} seconds")

        start_time = time.time()
        result = self.split_by_space(data)
        print(f"Time for split_by_space: {time.time() - start_time} seconds")

        return result

    def lower_case(self, data: str):
        return data.lower()

    def remove_non_ascii(self, data: str):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, data: str):
        return re.sub(r'[^\w\s]', '', data).strip()

    def correct_spelling(self, text: str):
        spell = SpellChecker()
        # Find those words in the text that may be misspelled
        misspelled = spell.unknown(text.split())
        corrected_text = text.split()

        for idx, word in enumerate(corrected_text):
            if word in misspelled:
                # Get the one `most likely` answer
                corrected_word = spell.correction(word)
                if corrected_word is None:
                    corrected_word = word  # Use the original word if correction fails
                corrected_text[idx] = corrected_word

        return ' '.join(corrected_text)

    def expand_contractions(self, text: str):
        return contractions.fix(text)

    def split_by_space(self, data: str):
        return data.split()

class CloseVocab(DataProcessing):
    # def process(self, data: str):
    #     return self.filter_words_in_vocab_database(self.split_by_space(
    #            self.expand_contractions(
    #            self.correct_spelling(
    #            self.remove_punctuation(
    #            self.remove_non_ascii(
    #            self.lower_case(data)))))))
    def process(self, data: str):
        start_time = time.time()
        data = self.lower_case(data)
        print(f"Time for lower_case: {time.time() - start_time} seconds")

        start_time = time.time()
        data = self.remove_non_ascii(data)
        print(f"Time for remove_non_ascii: {time.time() - start_time} seconds")

        start_time = time.time()
        data = self.remove_punctuation(data)
        print(f"Time for remove_punctuation: {time.time() - start_time} seconds")

        start_time = time.time()
        data = self.correct_spelling(data)
        print(f"Time for correct_spelling: {time.time() - start_time} seconds")

        start_time = time.time()
        data = self.expand_contractions(data)
        print(f"Time for expand_contractions: {time.time() - start_time} seconds")

        start_time = time.time()
        data = self.split_by_space(data)
        print(f"Time for split_by_space: {time.time() - start_time} seconds")

        start_time = time.time()
        result = self.filter_words_in_vocab_database(data)
        print(f"Time for filter_words_in_vocab_database: {time.time() - start_time} seconds")

        return result

    def lower_case(self, data: str):
        return data.lower()


    def remove_non_ascii(self, data: str):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, data: str):
        return re.sub(r'[^\w\s]', '', data).strip()

    def correct_spelling(self, text):
        spell = SpellChecker()
        # Find those words in the text that may be misspelled
        misspelled = spell.unknown(text.split())
        corrected_text = text.split()

        for idx, word in enumerate(corrected_text):
            if word in misspelled:
                # Get the one `most likely` answer
                corrected_word = spell.correction(word)
                if corrected_word is None:
                    corrected_word = word  # Use the original word if correction fails
                corrected_text[idx] = corrected_word

        return ' '.join(corrected_text)
    def filter_words_in_vocab_database(self,words):
        """ Filter a list of words to only include those that are in WordNet. """
        return [word for word in words if len(wn.synsets(word)) > 0]
    def expand_contractions(self,text):
        expanded_text = contractions.fix(text)
        return expanded_text
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
        array = []
        for i in tqdm.tqdm(data):
            array.append(self.clean(i))
        return array
    def saveData(self, data: str, name: str ):
        file_path = f'data/cleandata/{name}.pickle'
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
        print(f"data have been saved to {file_path} sucessfully")
if __name__ == "__main__":
    data = "Hello! This is an example sentence. (With some punctuation...)"
    cleaner = CleanData(CloseVocab())
    clean_data = cleaner.clean(data)
    print(clean_data)

