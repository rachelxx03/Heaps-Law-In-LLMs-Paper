
#tokenize it
#save it somewhere
import argparse
import json
import random
from loadData import DataLoaderFactory
from clean_data_strategy import SimpleProcessing


#choose randomly from the data
def select_random_elements(array, k):
    if len(array) < k:
        return "Array does not contain enough elements"
    return random.sample(array, k)
from abc import ABC, abstractmethod


class PromptStrategy(ABC):
    @abstractmethod
    def generate_prompt_single(self, item, command,length):
        pass

    def generate_prompt_array(self, item , command,length):
        pass

    @abstractmethod
    def generate_prompt_array(self, items):
        pass

    def save_prompt(self, prompt, file_name):
        # Ensure the directory exists
        import os
        os.makedirs("prompt", exist_ok=True)

        # Convert the list to a JSON string if it's not a string
        if not isinstance(prompt, str):
            prompt = json.dumps(prompt)

        with open("prompt/" + file_name, 'w') as file:
            file.write(prompt)

        return f"Prompt saved to {file_name}"

class ZeroShot(PromptStrategy):
    def generate_prompt_single(self, item, command,length):
        givenPrompt =command + item[0:length]
        return givenPrompt

    def generate_prompt_array(self, items , command,length):
        cleandata =SimpleProcessing()
        prompts = []
        for i in items:
            givenPrompt =command + " "+" ".join(cleandata.split_by_space(i)[0:length])
            prompts.append(givenPrompt)
        return prompts

class OneShot(PromptStrategy):
    def generate_prompt_single(self, item, command,length):
        examplePrompt =command + item +"\n"
        givenPrompt =examplePrompt + command + item[0:length]
        return givenPrompt

    def generate_prompt_array(self, items , command,length):
        prompts = []
        cleandata =SimpleProcessing()
        for i in items:
            examplePrompt =command +" " + i + " "
            givenPrompt =examplePrompt + command + " "+" ".join(cleandata.split_by_space(i)[0:length])
            prompts.append(givenPrompt)
        return prompts

class FewShot(PromptStrategy):
    def generate_prompt_single(self, item, command,length):
        examplePrompt =command + item +"\n"
        givenPrompt =examplePrompt + command + item[0:length]
        return givenPrompt

    def generate_prompt_array(self, items , command,length):
        prompts = []
        cleandata =SimpleProcessing()
        examplePrompt = ""

        for j in items[0:5]:
               examplePrompt +=command +" " + j + " "

        for i in items:
            givenPrompt =examplePrompt + command + " "+" ".join(cleandata.split_by_space(i)[0:length])
            prompts.append(givenPrompt)
        return prompts

class PromptContext:
    def __init__(self, strategy: PromptStrategy):
        self.strategy = strategy

    def generate_prompt_single(self, item, command,length):
        return self.strategy.generate_prompt_single(item, command,length)

    def generate_prompt_array(self, items , command,length):
        return self.strategy.generate_prompt_array(items, command,length)

    def save_strategy_output(self, prompt, file_name):
        return self.strategy.save_prompt(prompt, file_name)


def select_large_items(data, min_length=10, num_items=10000):
    # Filter items based on the minimum length requirement
    eligible_items = [item for item in data if len(item) > min_length]

    # Check if there are enough items to sample
    if len(eligible_items) < num_items:
        raise ValueError(f"Not enough items with length greater than {min_length}. Needed {num_items}, found {len(eligible_items)}.")

    # Randomly select num_items from the eligible items
    selected_items = random.sample(eligible_items, num_items)
    return selected_items

def generate_all_prompt(items ,name , command,length):
    promptStra = [ZeroShot(),OneShot(),FewShot()]
    namePrompt = ["zero_shot_","one_shot_", "few_shot_"]

    for i in range(len(promptStra)):
        promtS = PromptContext(strategy= promptStra[i])
        arr = promtS.generate_prompt_array(items , command,length)
        promtS.save_strategy_output(arr,namePrompt[i]+name)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--datasourse', type=int, default="0", help='choose where is the sourse of data')
    parser.add_argument('--inputdata', type=str, help='what is the name of the data')
    parser.add_argument('--choosedata', type=str, help='what is the name of the column?')
    parser.add_argument('--name', type=str, help='choose name for the outputfile')
    parser.add_argument('--prompt', type=str)

    args = parser.parse_args()
    #load data
    factory = DataLoaderFactory()
    loader = factory.get_loader(args.datasourse , args)  # args needs to be defined with appropriate attributes
    data = loader.load_data()
    result = select_large_items(data)
    generate_all_prompt(result,args.name,args.prompt,10)

