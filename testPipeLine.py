import json
import pickle

import numpy as np
import pandas as pd
from datasets import load_dataset
from HeapLawPlot import NonLinearLeastSquaresPlotStrategy, SimplePlotStrategy, LogLogPlotStrategy, \
    HeapsLawAnalyzer
import argparse
from clean_data_strategy import CleanData, SimpleProcessing, OpenVocab
from computeVocalAndTotalWord import computeVandT, NoDBCompute


def cleanData(data,name):
    cleaner = CleanData(SimpleProcessing())
    clean_data = cleaner.cleanTheArray(data)
    cleaner.saveData(clean_data,name)
    return clean_data

def ComputeData(rawData,name):
    compute = computeVandT(NoDBCompute())
    data = compute.executeStrategy(rawData)
    compute.saveData(data,name+"HeapsLaw")
    return data


def PlotHeapsLaw(Data,name):
    plot_strategy = [SimplePlotStrategy(), LogLogPlotStrategy() ]# Can be LogLogPlotStrategy, SimplePlotStrategy, or NonLinearLeastSquaresPlotStrategy
    plot_strategy_name = ["noneLogLog","LogLog"]
    for i in range(len(plot_strategy)):
        analyzer = HeapsLawAnalyzer(strategy=plot_strategy[i])
        name =plot_strategy_name[i] + name
        analyzer.perform_plot(Data,name)

    print("plot saved sucessfully")




def main(args):
    # Print a message args.count times
    for _ in range(args.count):
        print(f"Hello, {args.name}!")

def loadData(type):
    if type == 1 :
        my_dataset = load_dataset(args.inputdata)
        df = pd.DataFrame(my_dataset['train'])
        data = cleanData(df[args.choosedata][0:10000],args.name)
        return data

    elif type == 0:
        data = load_json(args.inputdata)
        df = pd.DataFrame(data)
        optimized_data = df.to_dict(orient='records')
        cleaned_data = cleanData(optimized_data, args.name)
        return cleaned_data
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--datasourse', type=int, default="0", help='choose where is the sourse of data')
    parser.add_argument('--inputdata', type=str, help='what is the name of the data')
    parser.add_argument('--choosedata', type=str, help='what is the name of the column?')
    parser.add_argument('--name', type=str, help='choose name for the outputfile')
    args = parser.parse_args()

    data = loadData(args.datasourse)
    newdata = ComputeData(data, args.name)
    PlotHeapsLaw(newdata, args.name)


