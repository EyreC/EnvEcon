#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Engine.py:

This file stores the Engine class.
"""

from Agent import *  # also imports EnvSymbols, and imports within EnvSymbols
from custom_timer import *
from UtilityHandler import *
from ErrorLogger import *
from AggregationManager import *

import datetime as dt
import random as rand
import math
from scipy.stats import beta, lognorm, norm
from tqdm import tqdm


class Engine:

    def __init__(self, num_agents, price, a_params, mu_params, income_interval, cG, cN, eG, eN, inflation_rate,
                 delta_interval=[0, 0], friend_interval=[0, 0]):
        """
        The Engine class represents the social system, composed of agents making decisions between e-commerce delivery
        options. The Engine has

        :param num_agents:      Number of agents interacting in the model
        :param price:           The average price of e-commerce goods
        :param a_params:        Beta distribution of shape parameters a and b for Alpha: preference for consumption
                                (coefficient of ln(Q))
        :param mu_params:       Min/ max bounds of mu, the eco-consciousness
        :param income_interval: Mean/ stdev of Y, disposable income
        :param cG:              The price per period of green delivery (say, monthly subscription price)
        :param cN:              The price per period of normal delivery (monthly subscription price)
        :param eG:              Emissions per unit of green delivery
        :param eN:              Emissions per unit of normal delivery
        :param inflation_rate:  The annual inflation rate of prices.
        :param delta_interval:  Min/ max bounds of delta, affinity towards friends' opinions
        :param friend_interval: Min/ max bounds of number of friends
        """
        print('Initialising engine')

        # Managers
        self.AggregationManager = AggregationManager(eG, eN, cG, cN)

        ##document variables
        self.Agents = [0 for i in range(num_agents)]
        self.Price = price
        self.A_params = a_params
        self.Mu_params = mu_params
        self.Income_int = income_interval
        self.Friend_int = friend_interval
        self.Delta_int = delta_interval

        self.GenerateAgents(num_agents)

        self.cG = cG
        self.cN = cN
        self.eG = eG
        self.eN = eN

        # inflation
        self.InflationRate = inflation_rate

        self.UtilityHandler = UtilityHandler()

    def GenerateAgents(self, num_agents):
        """
        Initiates n number of Agent objects within the Engine. The agents are initiated with affinity to consume,
        eco-consciousness

        :param num_agents:
        :return:
        """
        friendList = [j for j in range(num_agents)]
        for i in range(num_agents):
            a = beta.rvs(self.A_params[0], self.A_params[1])  # draw from beta distribution
            b = 1 - a

            # TODO: do we want eco-consciousness to be drawn from beta distribution?
            # mu = beta.rvs(self.Mu_params[0], self.Mu_params[1])
            mu = rand.uniform(self.Mu_params[0], self.Mu_params[1])

            income = np.exp(norm.rvs(self.Income_int[0], self.Income_int[1]))
            # income drawn from log-normal distribution, then exponentiated to get normal (level) income.

            delta = rand.uniform(self.Delta_int[0], self.Delta_int[1])

            agent = Agent(i, a, b, mu, income, self.Price, delta)

            # Assign friends
            friendList.remove(i)  # Agents cannot be friends with themselves
            agent.Friends = rand.sample(friendList, rand.choice(range(self.Friend_int[0], self.Friend_int[1])))
            friendList.append(i)

            self.Agents[i] = agent

    @timer
    def RunNormal(self, num_iterations):
        """
        Runs a simulation, where Agents make decisions on purchasing online goods and decide between a green or normal
        Prime subscription plan. The agents do NOT interact with each other on information exchange.

        :param num_iterations: Number of periods for which simulation is run.
        """
        print('\nRunning normal')

        self.UtilityHandler.SolveNormal()  # Sets up mathematical equations

        for i in range(num_iterations):  # for each period, for each agent...
            for agent in self.Agents:
                #  cG, cN, eG, eN
                agent.EnterGenericRound(i, self.cG, self.cN, self.eG, self.eN, self.UtilityHandler)

        self.ReportStatsAllStats(self.Agents, num_iterations)
        self.SaveStats(self.Agents, num_iterations, 'normal')
        self.SaveAgentSample(3, num_iterations, 'normal')

    def RunNormalWithIncomeScaling(self, num_iterations):
        """
        Runs a simulation where Income grows over time, where agents make deicions

        :param num_iterations:
        :return:
        """
        for i in range(num_iterations):
            for agent in tqdm(self.Agents):  # tqdm will time how long it takes to maximise each agent
                #  cG, cN, eG, eN
                agent.EnterRound(i, self.cG, self.cN, self.eG, self.eN)
                agent.UpdateBudget(i)
        self.ReportStatsAllStats(self.Agents, num_iterations)

    @timer  # Times the period for running the Social simulation
    def RunSocial(self, num_iterations):
        """
        Runs the Social simulation, where agents interact with each other on information exchange.

        :param num_iterations: Number of periods for which simulation is run
        """
        print('\nRunning social')

        self.UtilityHandler.SolveNormal()

        if num_iterations > 1:

            for agent in self.Agents:  # The first round is solved 'normally' without social effect
                agent.EnterGenericRound(0, self.cG, self.cN, self.eG, self.eN, self.UtilityHandler)
            self.UtilityHandler.SolveSocial()

            for i in range(num_iterations - 1):
                for agent in self.Agents:
                    # find this agent's friends
                    friends = [x for x in self.Agents if x.Id in agent.Friends]
                    agent.EnterSocialRound(i + 1, self.cG, self.cN, self.eG, self.eN, friends, self.UtilityHandler)
                    agent.UpdateBudget(i)
                self.InflatePrices(i)

        self.ReportStatsAllStats(self.Agents, num_iterations)
        self.SaveStats(self.Agents, num_iterations, 'social')
        self.SaveAgentSample(3, num_iterations, 'social')

    @timer
    def RunBenchMark(self, num_iterations):
        """
        The Benchmark simulation

        :param num_iterations: Number of periods for which to run the simulation for
        """
        print('\nRunning benchmark')

        self.UtilityHandler.SolveNormal()
        for i in range(num_iterations):
            for agent in self.Agents:
                agent.EnterBenchMarkRound(i, self.cN, self.eN, self.UtilityHandler)
                agent.UpdateBudget(i)
            self.InflatePrices(i)
        self.ReportStatsAllStats(self.Agents, num_iterations)
        self.SaveStats(self.Agents, num_iterations, 'benchmark')

    def InflatePrices(self, period):
        """
        Updates price of the average good each time this function is called (after every time period).
        Increases (price hikes) prices of Amazon plans at certain periodic intervals (defined in
        Constants.py)

        :param period: what period the current Engine is simulating
        """
        inf = ((self.InflationRate + 1) ** (
                    1 / 12)) - 1  # Inflation rate is given annually. Take monthly rate with CAGR

        self.Price = inf * self.Price
        if period % Constants.PriceHikeInterval() == 0 and period != 0:
            self.cG = inf ** Constants.PriceHikeInterval() * self.cG
            self.cN = inf ** Constants.PriceHikeInterval() * self.cN

    def PrintDeliveryShare(self):
        greens = 0
        for agent in self.Agents:
            if agent.CurrentPlan == "Green":
                greens += 1
        return f"Green Delivery: {greens}, Normal Delivery: {len(self.Agents) - greens}"

    def ReportStatsForPeriod(self, period):
        self.AggregationManager.ReportStatsForPeriod(self.Agents, period)

    def ReportStatsAllStats(self, agents, periods):
        self.AggregationManager.ReportAllStats(agents, periods)

    def SaveStats(self, agents, periods, type):
        self.AggregationManager.AddSimulationToCSV(agents, periods, type)

    def SaveAgentSample(self, sample_size, periods, type):
        self.AggregationManager.AddAgentSampleToCSV(self.Agents, sample_size, periods, type)
