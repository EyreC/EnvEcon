from Agent import *  # also imports EnvSymbols, and imports within EnvSymbols
from UtilityHandler import *
from ErrorLogger import *
from AggregationManager import *

import random as rand
import math
from scipy.stats import beta, lognorm, norm
from tqdm import tqdm
import datetime as dt


class Engine:

    def __init__(self, num_agents, price, a_interval, mu_interval, income_interval, cG, cN, eG, eN, inflation_rate, price_hike_interval,
                 delta_interval=[0, 0], friend_interval=[0, 0]):



        """
        The Engine class represents the social system, composed of agents making decisions between e-commerce delivery
        options. The Engine has

        :param num_agents:      Number of agents interacting in the model
        :param price:           Price
        :param a_interval:      Min/ max bounds of a, preference for consumption (coefficient of ln(Q))
        :param mu_interval:     Min/ max bounds of mu, preference for savings (coefficient of ln(S))
        :param income_interval: Min/ max bounds of Y, income
        :param cG:              Cost per unit of green delivery
        :param cN:              Cost per unit of normal delivery
        :param eG:              Emissions per unit of green delivery
        :param eN:              Emissions per unit of normal delivery
        :param omega_interval:  Min/ max bounds of omega,
        :param delta_interval:  Min/ max bounds of delta,
        :param friend_interval: Min/ max bounds of number of friends,
        """

        # Managers
        self.AggregationManager = AggregationManager(eG, eN)

        ##document variables
        self.Agents = [0 for i in range(num_agents)]
        self.Price = price
        self.A_int = a_interval
        self.Mu_int = mu_interval
        self.Income_int = income_interval
        self.Friend_int = friend_interval
        self.Delta_int = delta_interval

        self.GenerateAgents(num_agents)

        self.cG = cG
        self.cN = cN
        self.eG = eG
        self.eN = eN

        #inflation
        self.InflationRate = inflation_rate
        self.PriceHikeInterval = price_hike_interval

        self.UtilityHandler = UtilityHandler()

    def GenerateAgents(self, num_agents):
        friendList = [j for j in range(num_agents)]
        for i in range(num_agents):
            print(f"Generating agent {i}")
            # _id, a, b, mu, Y, p, friends = []):

            a = beta.rvs(self.A_int[0], self.A_int[1])  # replace with this line to draw from random beta distributino
            b = 1 - a
            mu = rand.uniform(self.Mu_int[0], self.Mu_int[1])
            income = np.exp(norm.rvs(self.Income_int[0], self.Income_int[1]))
            delta = rand.uniform(self.Delta_int[0], self.Delta_int[1])

            agent = Agent(i, a, b, mu, income, self.Price, delta)

            # assign friends
            friendList.remove(i)
            agent.Friends = rand.sample(friendList,  # Agents cannot be friends with themselves
                                   rand.choice(range(self.Friend_int[0], self.Friend_int[1])))
            friendList.append(i)

            self.Agents[i] = agent



    def RunNormal(self, num_iterations):
        self.UtilityHandler.SolveNormal()
        for i in range(num_iterations):
            for agent in tqdm(self.Agents):  # tqdm will time how long it takes to maximise each agent
                #  cG, cN, eG, eN
                #agent.EnterRound(i, self.cG, self.cN, self.eG, self.eN)
                agent.EnterGenericRound(i,self.cG, self.cN, self.eG, self.eN, self.UtilityHandler)
        self.ReportStatsAllStats(self.Agents, num_iterations)
        self.SaveStats(self.Agents, num_iterations, 'normal')

    def RunNormalWithIncomeScaling(self, num_iterations):
        for i in range(num_iterations):
            for agent in tqdm(self.Agents):  # tqdm will time how long it takes to maximise each agent
                #  cG, cN, eG, eN
                agent.EnterRound(i, self.cG, self.cN, self.eG, self.eN)
                agent.UpdateBudget(i)
        self.ReportStatsAllStats(self.Agents, num_iterations)
    @timer
    def RunSocial(self, num_iterations):
        self.UtilityHandler.SolveNormal()
        if num_iterations > 1:
            for agent in self.Agents:
                agent.EnterGenericRound(0, self.cG, self.cN, self.eG, self.eN, self.UtilityHandler)
            self.UtilityHandler.SolveSocial()
            for i in range (num_iterations - 1):
                print(f"Starting Social Round {i+1}")
                for agent in self.Agents:
                    # find this agent's friends
                    friends = [x for x in self.Agents if x.Id in agent.Friends]
                    agent.EnterSocialRound(i + 1, self.cG, self.cN, self.eG, self.eN, friends, self.UtilityHandler)
                    agent.UpdateBudget(i)
                self.InflatePrices(i)
        self.ReportStatsAllStats(self.Agents, num_iterations)
        self.SaveStats(self.Agents, num_iterations, 'social')
        self.SaveAgentSample(3, num_iterations, 'social')

    def RunBenchMark(self, num_iterations):
        self.UtilityHandler.SolveNormal()
        for i in range(num_iterations):
            for agent in self.Agents:
                agent.EnterBenchMarkRound(i, self.cN, self.eN, self.UtilityHandler)
        self.ReportStatsAllStats(self.Agents, num_iterations)
        self.SaveStats(self.Agents, num_iterations, 'benchmark')

    def InflatePrices(self, period):
        inf = 1 + self.InflationRate
        self.Price = inf * self.Price
        if period % self.PriceHikeInterval == 0 and period != 0:
            self.cG = inf * self.cG
            self.cN = inf * self.cN

    def PrintDeliveryShare(self):
        greens = 0
        for agent in self.Agents:
            if agent.CurrentPlan == "Green":
                greens += 1
        return f"Green Delivery: {greens}, Normal Delivery: {len(self.Agents) - greens}"

    def ReportStatsForPeriod(self, period):
        self.AggregationManager.ReportStatsForPeriod(self.Agents, period)

    def ReportStatsAllStats(self,agents, periods):
        self.AggregationManager.ReportAllStats(agents, periods)

    def SaveStats(self, agents, periods, type):
        self.AggregationManager.AddSimulationToCSV(agents, periods, type)

    def SaveAgentSample(self, sample_size, periods, type):
        self.AggregationManager.AddAgentSampleToCSV(self.Agents, sample_size, periods, type)


# if __name__ == '__main__':
#     mode, k = 0.75, 500  # mode and concentration
#
#     beta_distribution_a = (mode * (k-2)) + 1
#     beta_distribution_b = ((1-mode) * (k-2)) + 1
#
#     print('Initialising engine')
#     engine = Engine(10, 3, [0.3,0.7], [0.3,0.6], [300,500], 100,20, 0.01, 0.03,[0.3,0.8],[0.3,0.8],[1,2])
#     print('Starting normal rounds')
#     engine.RunNormalWithIncomeScaling(7)


