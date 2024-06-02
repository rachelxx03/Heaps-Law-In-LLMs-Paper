import pandas as pd
from datasets import load_dataset

data_files ={"train" : "train.csv" }
my_dataset = load_dataset("rachel6603/PubMed_10000", data_files = data_files)
print(my_dataset)
df = pd.DataFrame(my_dataset['train'])
#features: ['few_shot_pubmed_decoded_texts_default_key', 'one_shot_2_pubmed_decoded_texts_default_key', 'one_shot_pubmed_decoded_texts_default_key', 'zero_1_shot_pubmed_decoded_texts_default_key'],
