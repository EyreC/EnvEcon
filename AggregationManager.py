#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AggregationManager.py:

This file stores the AggregationManager class. The AggregationManager contains functions that reports the statistics of
the Engine and Agents, and saves the statistics to csv files under ./SavedStats.
"""

import pandas as pd
import numpy as np
import os as os
import random as rand


class AggregationManager:

    def __init__(self, eG, eN, cG, cN):
        self.eG = eG
        self.eN = eN
        self.cG = cG
        self.cN = cN

    def Reset(self, cG):
        self.cG = cG
    def AddAgentSampleToCSV(self, agents, sample_size, total_periods, type):
        if type == 'normal':
            filepath = './SavedStats/normal_agent.csv'
        elif type == 'social':
            filepath = './SavedStats/social_agent.csv'
        elif type == 'benchmark':
            filepath = './SavedStats/benchmark_agent.csv'

        # Grab a sample of agents
        sample_pool = rand.sample(agents, sample_size)
        sample_pool = sorted(sample_pool, key=lambda x: x.Id, reverse=False)

        cols = ['Period', 'AgentId', 'Budget', 'SelectedDeliveryPlan', 'UtilityIfGreen', 'UtilityIfNormal',
                'UtilityDisparity', 'Emissions', 'EcoCon']
        df = pd.DataFrame(columns=cols)

        for i, agent in enumerate(sample_pool):
            agent_df = pd.DataFrame(columns=cols)
            periods = [j for j in range(total_periods)]
            ids = [i for x in range(total_periods)]

            budgets_items = sorted([kv for kv in agent.BudgetHistory.items()], key=lambda x: x[0])
            budgets = [kv[1] for kv in budgets_items]

            utility_if_green_items = sorted([kv for kv in agent.GreenUtility.items()], key=lambda x: x[0])
            utility_if_green = [kv[1] for kv in utility_if_green_items]
            utility_if_normal_items = sorted([kv for kv in agent.NormalUtility.items()], key=lambda x: x[0])
            utility_if_normal = [kv[1] for kv in utility_if_normal_items]
            utility_disparity_items = sorted([kv for kv in agent.UtilityDisparity.items()], key=lambda x: x[0])
            utility_disparity = [kv[1] for kv in utility_disparity_items]

            emissions_items = sorted([kv for kv in agent.Erecords.items()], key=lambda x: x[0])
            emissions = [kv[1] for kv in emissions_items]
            plan_items = sorted([kv for kv in agent.PlanRecords.items()], key=lambda x: x[0])
            plan = [kv[1] for kv in plan_items]

            eco_con = [agent.EcoCon for i in periods]

            agent_df['Period'] = periods
            agent_df['AgentId'] = ids
            agent_df['Budget'] = budgets
            agent_df['SelectedDeliveryPlan'] = plan
            agent_df['UtilityIfGreen'] = utility_if_green
            agent_df['UtilityIfNormal'] = utility_if_normal
            agent_df['UtilityDisparity'] = utility_disparity
            agent_df['Emissions'] = emissions
            agent_df['EcoCon'] = eco_con

            df = pd.concat([df, agent_df], join='inner')

        df.to_csv(filepath, index=False)

    def AddSimulationToCSV(self, agents, total_periods, type):
        """
        Save simulation statistics to CSV

        :param agents:
        :param total_periods:
        :param type:
        :return:
        """
        if type == 'normal':
            filepath = './SavedStats/normal_simulation.csv'
        elif type == 'social':
            filepath = './SavedStats/social_simulation.csv'
        elif type == 'benchmark':
            filepath = './SavedStats/benchmark_simulation.csv'

        file_exists = os.path.exists(filepath)

        total_emissions = []
        total_utilities = []
        total_green = []
        total_normal = []
        total_green_q = []
        total_normal_q = []
        total_q = []

        for period in range(total_periods):

            incomes_list = [agent.BudgetHistory[period] for agent in agents]
            average_income = sum(incomes_list) / len(incomes_list)

            green_emissions = sum(
                [agent.Qrecords[period] * self.eG for agent in agents if agent.PlanRecords[period] == 'Green'])
            normal_emissions = sum(
                [agent.Qrecords[period] * self.eN for agent in agents if agent.PlanRecords[period] == 'Normal'])
            period_emissions = float(green_emissions + normal_emissions)

            green_utilities = sum(
                [agent.GreenUtility[period] for agent in agents if agent.PlanRecords[period] == 'Green'])
            normal_utilities = sum(
                [agent.NormalUtility[period] for agent in agents if agent.PlanRecords[period] == 'Normal'])
            period_utilities = float(green_utilities + normal_utilities)

            period_green = sum([1 for agent in agents if agent.PlanRecords[period] == 'Green'])
            period_normal = sum([1 for agent in agents if agent.PlanRecords[period] == 'Normal'])

            green_q = sum([agent.Qrecords[period] for agent in agents if agent.PlanRecords[period] == 'Green'])
            normal_q = sum([agent.Qrecords[period] for agent in agents if agent.PlanRecords[period] == 'Normal'])
            period_q = float(green_q + normal_q)

            total_emissions.append(period_emissions)
            total_utilities.append(period_utilities)
            total_green.append(period_green)
            total_normal.append(period_normal)

            total_green_q.append(green_q)
            total_normal_q.append(normal_q)
            total_q.append(period_q)

        df_dict = {
            'SimulationIndex': [0 for i in range(total_periods)],
            'PriceOfGreenDelivery': [self.cG for i in range(total_periods)],
            'PriceOfNormalDelivery': [self.cN for i in range(total_periods)],
            'Period': [i for i in range(total_periods)],
            'AverageIncome': average_income,
            'GreenUsers': total_green,
            'NormalUsers': total_normal,
            'TotalEmission': total_emissions,
            'TotalUtility': total_utilities,
            'QwithGreen': total_green_q,
            'QwithNormal': total_normal_q,
            'TotalQ': total_q
        }
        df = pd.DataFrame(df_dict)

        if file_exists:
            existing_df = pd.read_csv(filepath)

            prev_sim_index = max(existing_df['SimulationIndex'])  # previous simulation index

            simulation_index = [prev_sim_index + 1 for i in range(total_periods)]
            df['SimulationIndex'] = simulation_index
            save_df = pd.concat([existing_df, df], join='inner')

            save_df.to_csv(filepath, index= False)

        else:
            # add a column for the simulation number
            df['SimulationIndex'] = [0 for i in range(total_periods)]
            df.to_csv(filepath, index = False)

    # print num green delivery, normal delivery, total emissions
    def ReportStatsForPeriod(self, agents, period):
        """
        Report stats for a period (print df in terminal)

        :param agents:
        :param period:
        :return:
        """
        green_emissions = sum(
            [agent.Qrecords[period] * self.eG for agent in agents if agent.PlanRecords[period] == 'Green'])
        normal_emissions = sum(
            [agent.Qrecords[period] * self.eN for agent in agents if agent.PlanRecords[period] == 'Normal'])
        total_emissions = float(green_emissions + normal_emissions)

        green_utilities = sum(
            [agent.GreenUtility[period] for agent in agents if agent.PlanRecords[period] == 'Green'])
        normal_utilities = sum(
            [agent.NormalUtility[period] for agent in agents if agent.PlanRecords[period] == 'Normal'])
        total_utilities = float(green_utilities + normal_utilities)

        total_green = sum([1 for agent in agents if agent.PlanRecords[period] == 'Green'])
        total_normal = sum([1 for agent in agents if agent.PlanRecords[period] == 'Normal'])
        df_dict = {
            'TotalEmission': total_emissions,
            'TotalUtility': total_utilities,
            'GreenUsers': total_green,
            'NormalUsers': total_normal
        }
        df = pd.DataFrame(df_dict, index=[0])
        print(df)

    def ReportAllStats(self, agents, total_periods):
        """
        Report stats for all periods (print df in terminal)

        :param agents:
        :param total_periods:
        :return:
        """
        total_emissions = []
        total_utilities = []
        total_green = []
        total_normal = []

        for period in range(total_periods):
            green_emissions = sum(
                [agent.Qrecords[period] * self.eG for agent in agents if agent.PlanRecords[period] == 'Green'])
            normal_emissions = sum(
                [agent.Qrecords[period] * self.eN for agent in agents if agent.PlanRecords[period] == 'Normal'])
            period_emissions = float(green_emissions + normal_emissions)

            green_utilities = sum(
                [agent.GreenUtility[period] for agent in agents if agent.PlanRecords[period] == 'Green'])
            normal_utilities = sum(
                [agent.NormalUtility[period] for agent in agents if agent.PlanRecords[period] == 'Normal'])
            period_utilities = float(green_utilities + normal_utilities)

            period_green = sum([1 for agent in agents if agent.PlanRecords[period] == 'Green'])
            period_normal = sum([1 for agent in agents if agent.PlanRecords[period] == 'Normal'])

            total_emissions.append(period_emissions)
            total_utilities.append(period_utilities)
            total_green.append(period_green)
            total_normal.append(period_normal)

        df_dict = {
            'Period': [i for i in range(total_periods)],
            'TotalEmission': total_emissions,
            'TotalUtility': total_utilities,
            'GreenUsers': total_green,
            'NormalUsers': total_normal
        }
        df = pd.DataFrame(df_dict)
        df.set_index('Period', inplace=True)
        print(df)
