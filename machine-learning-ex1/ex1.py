import sys
import os

from functools import partial
import pandas
from matplotlib import pyplot as plt

'''
This script performs the tasks outline in ex1.pdf, from Coursera's machine learning course.
'''


def load(f, names=[]):
    '''Parse the data from the input file and store in pandas dataframs'''
    # Verify the file exist:
    try:
        _file = open(f, "r")
    except:
        print "ERROR: requested file {} does not exist or could not be opened."

    # Read the file into a pandas data frame
    # For this exercise, both files are csv format:

    if len(names) > 0:
        _data_frame = pandas.read_csv(f, header=None, names=names)
    else:
        _data_frame = pandas.read_csv(f, header=None)

    return _data_frame


def plotInitialData(df):
    # Now, let's plot the Profit as a function of the population:

    # Set up the plots
    fig, ax = plt.subplots(figsize=(10, 7))

    # Make a scatter plot
    ax.scatter(
        df['Population'], df['Profit'], label="Individual Truck Profits")

    # Plots require a title and axis labels:
    plt.title("Food Truck Profits", fontsize=30)
    plt.xlabel("Population of City (x10,000)", fontsize=20)
    plt.ylabel("Profit of City [$] (x10,000)", fontsize=20)

    # Make the ticks bigger to be more visible:
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    # Let's set the axis ranges a little more realistically:
    ax.set_xlim([5, 25])
    ax.set_ylim([-5, 30])

    # Need a legend, of course:
    plt.legend()

    plt.grid(True)

    plt.show()

# def updateCost(_series,_theta0,_theta1):

#   _series['cost'] = (_theta0 + _theta1*_series['Population'] - _series['Profit'])**2
#   return _series


def updateCost(_theta, _series):

    _series['cost'] = (
        _theta[0] + _theta[1]*_series['Population'] - _series['Profit'])**2
    return _series


def computeCost(df):
    '''Compute the cost of the data frame:
    '''
    cost = 1.0/(2*df.size)*df['cost'].sum()
    return cost


def updateParams(_alpha, _theta, _series):

    # Each theta has

    _series['diff0'] = \
        (_theta[0] + _theta[1]*_series['Population'] - _series['Profit'])*1
    _series['diff1'] = \
        (_theta[0] + _theta[1]*_series['Population'] -
         _series['Profit'])*_series['Profit']


def main():
    # First, read the data needed for this data set:
    _file = "ex1/ex1data1.txt"
    df = load(_file, ["Population", "Profit"])

    # Let's see what's inside:
    # df.info()

    # plotInitialData(df)

    '''
  Now, move on to the model of linear regression:
  I'm going to do this entirely with the data frame and the parameters theta0, theta1
  I'll have a column for the cost computation, and two columns for updating
  the theta parameters
  '''

    learning_rate = 0.01
    theta = (0, 0)

    # To make the linear regression work well,

    # This is a cool trick.  Apply will automatically unpack
    # extra variables and arguments into a flat list.
    # That's not ideal, since we will want to generalize the way
    # the cost is computed later for multiple variables.
    #
    # Instead, make a partial function out of the needed function, with the
    # theta parameters already supplied.  Pandas just has to pass the data
    # frame, now.
    df = df.apply(partial(updateCost, theta), axis=1)

    print "Initial cost is {:.3}".format(computeCost(df))


if __name__ == '__main__':
    main()
