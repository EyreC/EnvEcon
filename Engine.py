import math as ma
import sympy as sp
from sympy import *
#init_printing()
import random as rand
from Agent import *
from EnvSymbols import *

class Engine:
    def __init__(self, num_agents, price, a_interval, mu_interval, income_interval,
                 cG, cN, eG, eN, omega_interval=[0, 0], delta_interval=[0, 0], friend_interval=[0, 0]):

        ##document variables
        self.Agents = []
        self.Price = price
        self.A_int = a_interval
        self.Mu_int = mu_interval
        self.Income_int = income_interval
        self.Friend_int = friend_interval
        self.Omega_int = omega_interval
        self.Delta_int = delta_interval

        self.GenerateAgents(num_agents)

        self.cG = cG
        self.cN = cN
        self.eG = eG
        self.eN = eN

    def GenerateAgents(self, num_agents):
        for i in range(num_agents):
            # _id, a,b,mu, Y, p, friends = []):
            a = rand.uniform(self.A_int[0], self.A_int[1])
            b = 1. - a
            mu = rand.uniform(self.Mu_int[0], self.Mu_int[1])
            income = rand.uniform(self.Income_int[0], self.Income_int[1])
            omega = rand.uniform(self.Omega_int[0], self.Omega_int[1])
            delta = rand.uniform(self.Delta_int[0], self.Delta_int[1])

            agent = Agent(i, a, b, mu, income, self.Price, omega, delta)
            ## todo Justin, random sample
            friends = list(set([rand.choice(range(num_agents)) for x in
                                range(rand.choice(range(self.Friend_int[0], self.Friend_int[1])))]))
            agent.Friends = friends
            self.Agents.append(agent)

    def RunNormal(self, num_iterations):
        for i in range(num_iterations):
            for agent in self.Agents:
                #  cG, cN, eG, eN
                agent.EnterRound(i, self.cG, self.cN, self.eG, self.eN)

    def RunSocial(self, num_iterations):
        for i in range(num_iterations):
            if i == 0:
                for agent in self.Agents:
                    agent.EnterRound(i, self.cG, self.cN, self.eG, self.eN)
            else:
                for agent in self.Agents:
                    # find this agent's friends
                    friends = (x for x in self.Agents if x.Id in agent.Friends)
                    agent.EnterSocialRound(i, self.cG, self.cN, self.eG, self.eN, friends)

    def RunRebound(self, num_iterations):
        return

    def ResetAgents(self):
        # reset
        return

    def PrintDeliveryShare(self):
        greens = 0
        for agent in self.Agents:
            if agent.CurrentPlan == "Green":
                greens += 1
        return f"Green Delivery: {greens}, Normal Delivery: {len(self.Agents) - greens}"