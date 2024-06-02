import argparse
import json
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import os
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from loadData import DataLoaderFactory


class Data_Selection:
    def __init__(self, args, limit=400):
        self.name = args.name
        self.doc_counts = {}
        self.first_2_sentence = {}
        factory = DataLoaderFactory()
        data_loader = factory.get_loader(args)
        self.data = data_loader.load_data()
        self.limit = limit

    def save_data(self, data, name):
        filename = name
        # Open a file for writing
        with open(filename, 'w') as f:
            # Use json.dump to write the data to a file
            json.dump(data, f)
        print("Data has been saved under: " + filename)

#not complete due to its no reuseable
    def limit_number_of_word(self):
        limited_data = []

        for doc in tqdm(self.data):
            number_of_words = len(doc.split(" "))
            if number_of_words >= self.limit:
                limited_data.append(doc)

        # Set seed for reproducibility
        random.seed(42)
        # Choose a random subset of 60000 elements
        if len(limited_data) > 60000:
            limited_data = random.sample(limited_data, 60000)

        print(len(limited_data))
        filename = "data/selectedData/" + str(self.limit) + "_"+self.name
        self.save_data(limited_data,filename)
        return limited_data

    #still hard code number
    def divide_and_save_data(self,data):
        # Shuffle the limited data to randomize the order
        random.shuffle(data)

        # Split the data
        subset_10000 = data[:10000]
        remaining_50000 = data[10000:]

        # Save the subsets to files
        self.save_data(subset_10000, f"data/selectedData/{self.limit}_subset_10000_{self.name}.json")
        self.save_data(remaining_50000, f"data/selectedData/{self.limit}_remaining_50000_{self.name}.json")



    def analyze_texts(self,texts):
        first_two_sentences_lengths = []
        post_first_two_sentences_lengths = []

        for text in texts:
            sentences = sent_tokenize(text)

            # Calculate the length of the first two sentences
            first_two = ' '.join(sentences[:2])
            first_two_length = len(first_two)
            first_two_sentences_lengths.append(first_two_length)

            # Calculate the length of the text after the first two sentences
            remaining_text = ' '.join(sentences[2:])
            remaining_text_length = len(remaining_text)
            post_first_two_sentences_lengths.append(remaining_text_length)

        # Calculate averages
        average_length_initial = sum(first_two_sentences_lengths) / len(first_two_sentences_lengths)
        average_length_remaining = sum(post_first_two_sentences_lengths) / len(post_first_two_sentences_lengths)

        return first_two_sentences_lengths, post_first_two_sentences_lengths, average_length_initial, average_length_remaining



    def calculate_number_of_words(self):
        for data in self.data:
            number_of_words = len(data.split(" "))
            if self.doc_counts.get(number_of_words) is None:
                self.doc_counts[number_of_words] = 1
            else:
                self.doc_counts[number_of_words] += 1

    # def plot_the_first_2_sentence(self):
    def plot_lengths(self,initial_lengths, remaining_lengths):
        directory = 'data/dataPlot'
        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.figure(figsize=(10, 5))
        plt.plot(initial_lengths, label='First Two Sentences Length')
        plt.plot(remaining_lengths, label='Post First Two Sentences Length')
        plt.title('Comparison of Text Lengths')
        plt.xlabel('Document Index')
        plt.ylabel('Length of Text')
        plt.legend()

        plot_path = os.path.join(directory, self.name + '_length_word_count_histogram.png')
        plt.savefig(plot_path)
        plt.show()



    def plot_word_counts(self):
        """Plots a histogram of document counts by their word counts."""
        # Ensure the directory exists
        directory = 'data/dataPlot'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Sorting the keys for better visualization
        word_lengths = sorted(self.doc_counts.keys())
        counts = [self.doc_counts[length] for length in word_lengths]

        plt.figure(figsize=(10, 6))
        plt.bar(word_lengths, counts, color='blue')
        plt.title('Number of Documents by Word Count')
        plt.xlabel('Number of Words in Document')
        plt.ylabel('Number of Documents')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()

        # Saving the plot
        plot_path = os.path.join(directory, self.name + '_doc_word_count_histogram.png')
        plt.savefig(plot_path)
        plt.close()  # Close the figure to free up memory
        print("plot have been saved under: "+ str(directory) +str( self.name + '_doc_word_count_histogram.png'))
        return plot_path





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--datasourse', type=int, default="0", help='choose where is the sourse of data')
    parser.add_argument('--inputdata', type=str, help='what is the name of the data')
    parser.add_argument('--choosedata', type=str, help='what is the name of the column?')
    parser.add_argument('--name', type=str, help='what is the name of the column?')

    args = parser.parse_args()

    data_selector = Data_Selection(args)
    data_selector.calculate_number_of_words()
    result_path = data_selector.plot_word_counts()
    x = data_selector.limit_number_of_word()
    first_two_lengths, remaining_lengths, avg_initial, avg_remaining = data_selector.analyze_texts(x)
    print("Average length of the first two sentences: ", avg_initial)
    print("Average length of remaining text: ", avg_remaining)
    data_selector.plot_lengths(first_two_lengths, remaining_lengths)
    data_selector.divide_and_save_data(x)
