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


def agent_plotter(df, plot_type, group_type):
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.set_title(f'Agent {plot_type} by {group_type}')
    ax.set_ylabel(f'{plot_type}')
    ax.set_xlabel('Period')

    num_of_agents = len(df['AgentId'].unique())
    periods = len(df['Period'].unique())
    period_array = [i for i in range(periods)]

    is_first_high = True
    is_first_med = True
    is_first_low = True
    is_first_arr = [is_first_high, is_first_med, is_first_low]

    for i in range(num_of_agents):
        # get agent data
        agent_data = df.loc[df['AgentId'] == i]
        high_med_low = get_high_med_low(agent_data, group_type)
        color = get_color(group_type, high_med_low)
        if plot_type == 'Emissions':
            emissions = agent_data['Emissions']
            plot_data(ax, period_array, emissions, color, high_med_low, is_first_arr)
            # ax.plot(period_array, emissions, c=color)
            # ax.scatter(period_array, emissions,c=color)
        elif plot_type == 'Utility Disparity':
            utility_disparity = agent_data['UtilityDisparity']
            plot_data(ax, period_array, utility_disparity, color, high_med_low, is_first_arr)
            ax.plot(period_array, utility_disparity, c=color)
            ax.scatter(period_array, utility_disparity, c=color)

    # plot zero line
    zero_line = [0 for i in period_array]
    ax.plot(period_array, zero_line, c='k', label='Zero Line')

    ax.legend(loc='upper left')


def plot_data(ax, period_array, data, color, var_type, is_first_arr):
    if var_type == "High":
        ax.scatter(period_array, data, c=color)
        if is_first_arr[0]:
            ax.plot(period_array, data, c=color, label='High')
            is_first_arr[0] = False
        else:
            ax.plot(period_array, data, c=color)
    elif var_type == 'Medium':
        ax.scatter(period_array, data, c=color)
        if is_first_arr[1]:
            ax.plot(period_array, data, c=color, label='Medium')
            is_first_arr[1] = False
        else:
            ax.plot(period_array, data, c=color)
    elif var_type == "Low":
        ax.scatter(period_array, data, c=color)
        if is_first_arr[2]:
            ax.plot(period_array, data, c=color, label='Low')
            is_first_arr[2] = False
        else:
            ax.plot(period_array, data, c=color)


def get_high_med_low(agent_data, group_type):
    if group_type == 'Income':
        return get_income_type(agent_data)
    elif group_type == 'Eco Consciousness':
        return get_eco_type(agent_data)


def get_income_type(agent_data):
    final_period_budget = agent_data['Budget'].iloc[-1]
    if final_period_budget > 5500:
        return 'High'
    elif final_period_budget > 2000:
        return 'Medium'
    else:
        return 'Low'


def get_eco_type(agent_data):
    eco_con = agent_data['EcoCon'].iloc[-1]
    if eco_con > 0.006:
        return 'High'
    elif eco_con > 0.004:
        return 'Medium'
    else:
        return 'Low'


def get_color(group_type, var_type):
    if group_type == 'Income':
        return get_color_from_high_mid_low(var_type)

    elif group_type == 'Eco Consciousness':
        return get_color_from_high_mid_low(var_type)


def get_color_from_high_mid_low(var_type):
    if var_type == "High":
        return 'b'
    elif var_type == 'Medium':
        return 'm'
    elif var_type == "Low":
        return 'c'

