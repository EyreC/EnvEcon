import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
%matplotlib inline

def aggregate_emissions(df):
    return df.groupby('Period').agg({'TotalEmission':np.mean})['TotalEmission']

def emissions_plotter(dfs, labels):
    fig, ax = plt.subplots()

    ax.set_title('Aggregate Emissions')
    ax.set_ylabel('Emissions')
    ax.set_xlabel('Period')

    for i, df in enumerate(dfs):
        emissions = aggregate_emissions(df)
        periods = [i for i in range(len(emissions))]

        ax.plot(periods, emissions, label=labels[i])
        ax.scatter(periods, emissions)
    ax.legend(loc='upper left')

