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

    def __init__(self, num_agents, price, a_interval, mu_interval, income_interval, cG, cN, eG, eN,
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
        self.Agents = []
        self.Price = price
        # self.A_shape_params = (a, b)
        self.A_int = a_interval
        self.Mu_int = mu_interval
        self.Income_int = income_interval
        self.Friend_int = friend_interval
        self.Delta_int = delta_interval

        self.GenerateAgents(num_agents)
        # print status of agents

        self.cG = nsimplify(cG)
        self.cN = nsimplify(cN)
        self.eG = nsimplify(eG)
        self.eN = nsimplify(eN)

        self.UtilityHandler = UtilityHandler()

    def GenerateAgents(self, num_agents):
        ## the nsimplify method converts floats into rational numbers
        ## e.g. 0.3 -> 3/10
        # this helps sympy solvers run more quickly
        for i in range(num_agents):
            # _id, a, b, mu, Y, p, friends = []):

            # a = beta.rvs(self.A_params[0], self.A_params[1])  # replace with this line to draw from random beta distributino
            a = nsimplify(rand.uniform(self.A_int[0], self.A_int[1]))
            b = 1 - a
            mu = nsimplify(rand.uniform(self.Mu_int[0], self.Mu_int[1]))

            # income = nsimplify(rand.uniform(self.Income_int[0], self.Income_int[1]))
            income = np.exp(norm.rvs(self.Income_int[0], self.Income_int[1]))

            delta = nsimplify(rand.uniform(self.Delta_int[0], self.Delta_int[1]))

            agent = Agent(i, a, b, mu, income, self.Price, delta)
            ## todo Justin, random sample
            # This should be able to do the same job as list set
            friends = rand.sample([j for j in range(num_agents) if j!=i],  # Agents cannot be friends with themselves
                                   rand.choice(range(self.Friend_int[0], self.Friend_int[1])))

            friends2 = list(set([rand.choice(range(num_agents)) for x in
                                range(rand.choice(range(self.Friend_int[0], self.Friend_int[1])))]))


            agent.Friends = friends


            self.Agents.append(agent)



    def RunNormal(self, num_iterations):
        self.UtilityHandler.SolveNormal()
        for i in range(num_iterations):
            for agent in tqdm(self.Agents):  # tqdm will time how long it takes to maximise each agent
                #  cG, cN, eG, eN
                #agent.EnterRound(i, self.cG, self.cN, self.eG, self.eN)
                agent.EnterGenericRound(i,self.cG, self.cN, self.eG, self.eN, self.UtilityHandler)
        self.ReportStatsAllStats(self.Agents, num_iterations)

    def RunNormalWithIncomeScaling(self, num_iterations):
        for i in range(num_iterations):
            for agent in tqdm(self.Agents):  # tqdm will time how long it takes to maximise each agent
                #  cG, cN, eG, eN
                agent.EnterRound(i, self.cG, self.cN, self.eG, self.eN)
                agent.UpdateBudget(i)
        self.ReportStatsAllStats(self.Agents, num_iterations)

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
        self.ReportStatsAllStats(self.Agents, num_iterations)

    def RunBenchMark(self, num_iterations):
        self.UtilityHandler.SolveNormal()
        for i in range(num_iterations):
            for agent in self.Agents:
                agent.EnterBenchMarkRound(i, self.cN, self.eN, self.UtilityHandler)
        self.ReportStatsAllStats(self.Agents, num_iterations)


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


