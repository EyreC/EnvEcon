#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent.py:

This file stores the Agent class.
"""

from EnvSymbols import *  # Also imports math and sympy
from Constants import *


class Agent:

    def __init__(self, _id, a, b, mu, Y, p, delta=0, friends=[]):
        """
        Initialises an Agent object with the following attributes:

        :param _id: Unique identifier
        :param a: Preference for consumption (coefficient of ln[Q])
        :param b: Preference for savings (coefficient of ln[S])
        :param mu: Eco-consicousness
        :param Y: Disposable income
        :param p: Average price of
        :param omega:
        :param delta:
        :param friends: a list of agent ids who the Agent values the opinion of
        """
        print(f"Initialising agent {_id}")

        self.Id = _id

        # Expression variables
        self.Budget = Y
        self.A = a
        self.B = b
       # self.UtilityExpr = a * ln(Q) + b * ln(S) - a*ln(mu * e_rate * Q + 1)
        self.Price = p
        self.EcoCon = mu

        # Current period props
        self.CurrentPlan = 'Normal'  # plan defaults to normal delivery
        self.CurrentUtility = 0

        # Friendship
        self.Friends = []
        self.Delta = delta
        self.Friend_Effect = None

        # History
        self.Qrecords = {}
        self.Srecords = {}
        self.BudgetHistory = {}
        self.PlanRecords = {}
        self.GreenUtility = {}
        self.NormalUtility = {}
        self.GenericUtility = {}

        self.UtilityDisparity = {}
        self.Erecords = {}

        # ErrorLogger

    def EnterGenericRound(self, period, cG, cN, eG, eN, utility_handler):
        self.CurrentUtility = self.compare_generic(period, cG, cN, eG, eN, utility_handler)

    def compare_generic(self, period, cG, cN, eG, eN, utility_handler):
        util_green, util_normal = self.evaluate_green_normal(utility_handler, cG, cN, eG, eN)

        # compare utilities
        green_is_better = util_green > util_normal  # and util_green != util_normal  # I think this second operation is redundant

        if green_is_better:
            self.assign_green(period, utility_handler, eG, cG)
            self.assign_budget_and_utilities_disparity(period, util_green, util_normal)
            return util_green

        else:
            self.normal = self.assign_normal(period, utility_handler, eN, cN)  # TODO: don't need "self.normal ="?
            self.assign_budget_and_utilities_disparity(period, util_green, util_normal)
            return util_normal
    
    def evaluate_green_normal(self, utility_handler, cG, cN, eG, eN):
        util_green = utility_handler.LambdifyNormal(self.A, self.B, self.EcoCon, self.Budget, self.Price, eG, cG)
        util_normal = utility_handler.LambdifyNormal(self.A, self.B, self.EcoCon, self.Budget, self.Price, eN, cN)
        return util_green, util_normal
    
    def assign_green(self, period, utility_handler, eG, cG):
        self.CurrentPlan = 'Green'
        self.PlanRecords[period] = 'Green'
        self.Qrecords[period] = utility_handler.Lambdify_Q(self.A, self.B, self.EcoCon, self.Budget, self.Price, eG, cG)
        self.Srecords[period] = utility_handler.Lambdify_S(self.A, self.B, self.EcoCon, self.Budget, self.Price, eG, cG)
        self.Erecords[period] = self.Qrecords[period] * eG

    def assign_normal(self, period, utility_handler, eN, cN):
        """

        :param period:
        :param utility_handler:
        :param eN:
        :param cN:
        :return:
        """
        self.CurrentPlan = 'Normal'
        self.PlanRecords[period] = 'Normal'
        self.Qrecords[period] = utility_handler.Lambdify_Q(self.A, self.B, self.EcoCon, self.Budget, self.Price, eN, cN)
        self.Srecords[period] = utility_handler.Lambdify_S(self.A, self.B, self.EcoCon, self.Budget, self.Price, eN, cN)
        self.Erecords[period] = self.Qrecords[period] * eN

    def assign_budget_and_utilities_disparity(self, period, util_green, util_normal):
        """
        Record the agent's budget, their utility from choosing green or normal, and the difference between these two
        utilities (util_green - util_normal), called util_disparity.
        If util_normal > util_green, util_disparity < 0

        :param period:  current period index
        :param util_green:  utility choosing green plan
        :param util_normal:  utility choosing normal plan
        :return: None
        """
        self.BudgetHistory[period] = self.Budget
        self.GreenUtility[period] = util_green
        self.NormalUtility[period] = util_normal
        self.UtilityDisparity[period] = util_green - util_normal

    def assign_choice(self):
        return

    
    def EnterSocialRound(self, period, cG, cN, eG, eN, friends, utility_handler):
        """
        At each period (round),

        :param period:
        :param cG:
        :param cN:
        :param eG:
        :param eN:
        :param friends:
        :return:
        """
        self.CurrentUtility = self.compare_generic_social(period, cG, cN, eG, eN, friends, utility_handler)

    def compare_generic_social(self, period, cG, cN, eG, eN, friends, utility_handler):
        # Eval utility for green delivery
        util_green, util_normal = self.evaluate_green_normal_social(utility_handler, cG, cN, eG, eN, friends, period)

        # compare utilities
        green_is_better = util_green > util_normal  # and util_green != util_normal  # I think this second operation is redundant

        if green_is_better:
            self.assign_green_social(period, utility_handler, eG, cG)
            self.assign_budget_and_utilities_disparity(period, util_green, util_normal)
            return util_green

        else:
            self.assign_normal_social(period, utility_handler, eN, cN)
            self.assign_budget_and_utilities_disparity(period, util_green, util_normal)
            return util_normal

    def evaluate_green_normal_social(self, utility_handler, cG, cN, eG, eN, friends, period):
        util_green = utility_handler.LambdifySocial(self.A, self.B, self.EcoCon, self.Budget, self.Price, eG, cG,
                                                    self.Delta,
                                                    sum([1 for friend in friends if
                                                         friend.PlanRecords[period - 1] == 'Green']) / len(friends))
        util_normal = utility_handler.LambdifySocial(self.A, self.B, self.EcoCon, self.Budget, self.Price, eN, cN,
                                                     self.Delta,
                                                     sum([1 for friend in friends if
                                                          friend.PlanRecords[period - 1] == 'Normal']) / len(friends))

        return util_green, util_normal

    def assign_green_social(self, period, utility_handler, eG, cG):
        self.assign_green(period, utility_handler, eG, cG)

    def assign_normal_social(self, period, utility_handler, eN, cN):
        self.assign_normal(period, utility_handler, eN, cN)

    
    def EnterBenchMarkRound(self, period, cN, eN, utility_handler):
        self.CurrentUtility = self.compare_normal_to_no_plan(period, cN, eN, utility_handler)

    def compare_normal_to_no_plan(self, period, cN, eN, utility_handler):
        util_normal = utility_handler.LambdifyNormal(self.A, self.B, self.EcoCon, self.Budget, self.Price, eN, cN)

        if util_normal > 0:
            self.assign_normal(period, utility_handler, eN, cN)
            self.assign_budget_and_utilities_disparity(period, 0, util_normal)
        else:
            self.CurrentPlan = 'None'
            self.PlanRecords[period] = 'None'
            self.Qrecords[period] = 0
            self.Srecords[period] = self.Budget
            self.assign_budget_and_utilities_disparity(period, 0, util_normal)

    def UpdateBudget(self,period):
        # add savings
        self.Budget += Constants.FractionOfSavings() * self.Srecords[period]