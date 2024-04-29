import pickle
import pandas as pd
from datasets import load_dataset
from HeapLawPlot import NonLinearLeastSquaresPlotStrategy, SimplePlotStrategy, LogLogPlotStrategy, \
    HeapsLawAnalyzer

from clean_data_strategy import CleanData, SimpleProcessing
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
    plot_strategy = [NonLinearLeastSquaresPlotStrategy(), SimplePlotStrategy(), LogLogPlotStrategy() ]# Can be LogLogPlotStrategy, SimplePlotStrategy, or NonLinearLeastSquaresPlotStrategy
    plot_strategy_name = ["leastSquare","noneLogLog","LogLog"]
    for i in range(len(plot_strategy)):
        analyzer = HeapsLawAnalyzer(strategy=plot_strategy[i])
        name =plot_strategy_name[i] + name
        analyzer.perform_plot(Data,name)

    print("plot saved sucessfully")


import argparse

def main(args):
    # Print a message args.count times
    for _ in range(args.count):
        print(f"Hello, {args.name}!")

def loadData(type):
    if type == 1 :
        my_dataset = load_dataset(args.inputdata)
        df = pd.DataFrame(my_dataset['train'])
        data = cleanData(df[args.choosedata],args.name)
        return data
    elif type == 0:
        pass



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

