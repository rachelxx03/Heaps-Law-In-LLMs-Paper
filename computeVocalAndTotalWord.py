import pickle
import random
import sqlite3

class ComputeVocabAndTotalWord:
    def process(self, data):
        """Process the data to compute total words and unique vocab count."""
        raise NotImplementedError("Subclasses must override process()")

class NoDBCompute(ComputeVocabAndTotalWord):
    def process(self, data):
        newarray = []
        overall_total_words = 0
        overall_unique_words = set()

        for word_array in data:
                overall_total_words += len(word_array)
                overall_unique_words.update(word_array)
                newarray.append([overall_total_words,len(overall_unique_words)])


        return newarray

class SQLiteCompute(ComputeVocabAndTotalWord):
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')  # Use in-memory database for demonstration
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE words (word TEXT UNIQUE)')

    def process(self, data):
        overall_total_words = 0

        for word_array in data:
            overall_total_words += len(word_array)
            for word in word_array:
                try:
                    self.cursor.execute('INSERT INTO words (word) VALUES (?)', (word,))
                except sqlite3.IntegrityError:
                    pass  # Ignore duplicates

        self.cursor.execute('SELECT COUNT(*) FROM words')
        unique_word_count = self.cursor.fetchone()[0]
        return overall_total_words, unique_word_count

    def close(self):
        self.conn.close()

class computeVandT:
    def __init__(self, strategy):
        self.strategy = strategy

    def setStrategy(self, strategy):
        self.strategy = strategy

    def executeStrategy(self, data):
        return self.strategy.process(data)

    def executeOnAnArray(self,data):
        return  [self.executeStrategy(i) for i in data]

    def saveData(self, data: str, name: str ):
        file_path = f'data/heapLawData/{name}.pickle'
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
        print(f"data have been saved to {file_path} sucessfully")


