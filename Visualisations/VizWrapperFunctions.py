#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VizWrapperFunctions.py:

This file contains functions that assist with visualisations.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# %matplotlib inline

def aggregate_emissions(df):
    """
    Aggregates the emissions grouped by Period.

    :param df: a Pandas dataframe with which to aggregate emissions
    :return:
    """
    return df.groupby('Period').agg({'TotalEmission': np.mean})['TotalEmission']


def aggregate_utility(df):
    """
    Aggregates utility grouped by Period

    :param df: a Pandas dataframe with which to aggregate utility
    :return:
    """
    return df.groupby('Period').agg({'TotalUtility': np.mean})['TotalUtility']


def emissions_plotter(dfs: list, labels: list):
    fig, ax = plt.subplots()

    ax.set_title('Aggregate emissions over time')
    ax.set_ylabel('Emissions')
    ax.set_xlabel('Period')

    for i, df in enumerate(dfs):
        emissions = aggregate_emissions(df)
        periods = periods = df.Period.unique()

        ax.plot(periods, emissions, label=labels[i])
        ax.scatter(periods, emissions)
    ax.legend(loc='upper left')


def utilities_plotter(dfs: list, labels: list):
    fig, ax = plt.subplots()

    ax.set_title('Aggregate utility over time')
    ax.set_ylabel('Utility')
    ax.set_xlabel('Period')
    for i, df in enumerate(dfs):
        utilities = aggregate_utility(df)
        periods = df.Period.unique()

        ax.plot(periods, utilities, label=labels[i])
        ax.scatter(periods, utilities)
    ax.legend(loc='upper left')


def aggregate_emissions_by_green_delivery_price(df):
    max_period = df['Period'].max()
    df = df[df['Period'] == max_period]
    return df.groupby('PriceOfGreenDelivery').agg({'TotalEmission': np.mean})['TotalEmission']


def aggregate_utility_by_green_delivery_price(df):
    max_period = df['Period'].max()
    df = df[df['Period'] == max_period]
    return df.groupby('PriceOfGreenDelivery').agg({'TotalUtility': np.mean})['TotalUtility']


def emissions_by_green_delivery_price_plotter(dfs: list, labels: list):
    """
    How does emissions change according to the different prices of green delivery
    """
    fig, ax = plt.subplots()

    max_period = dfs[0]['Period'].max()

    ax.set_title(f'Emissions after {max_period} periods, by price')
    ax.set_ylabel('Total emissions')
    ax.set_xlabel('Price of green delivery')
    for i, df in enumerate(dfs):
        emissions = aggregate_emissions_by_green_delivery_price(df)
        prices = df.PriceOfGreenDelivery.unique()

        ax.plot(prices, emissions, label=labels[i])
        ax.scatter(prices, emissions)
    ax.legend(loc='upper left')



def aggregate_green_adopters_by_green_delivery_price(df):
    max_period = df['Period'].max()  # Find number of green adopters in the latest period
    df = df[df['Period'] == max_period]
    green_users = df.groupby('PriceOfGreenDelivery').agg({'GreenUsers': np.mean})['GreenUsers']
    normal_users = df.groupby('PriceOfGreenDelivery').agg({'NormalUsers': np.mean})['NormalUsers']
    return green_users / (green_users + normal_users)



def green_adopters_by_green_delivery_price_plotter(dfs: list, labels: list):
    fig, ax = plt.subplots()

    max_period = dfs[0]['Period'].max()

    ax.set_title(f'Emissions after {max_period + 1} periods, by price')
    ax.set_ylabel('Proportion of agents adoption green delivery')
    ax.set_xlabel('Price of green delivery')
    for i, df in enumerate(dfs):
        proportion_green = aggregate_emissions_by_green_delivery_price(df)
        prices = df.PriceOfGreenDelivery.unique()

        ax.plot(prices, proportion_green, label=labels[i])
        ax.scatter(prices, proportion_green)
    ax.legend(loc='upper left')