from EnvSymbols import *  # Also imports math and sympy


class Agent:

    def __init__(self, _id, a, b, mu, Y, p, delta=0, friends=[]):
        """
        Initialises an Agent object with the following attributes:

        :param _id: Unique identifier
        :param a: Preference for consumption (coefficient of ln[Q])
        :param b: Preference for savings (coefficient of ln[S])
        :param mu: Eco-consicousness
        :param Y: Income
        :param p: price of green delivery
        :param omega:
        :param delta:
        :param friends: a list of agent ids who the Agent values the opinion of
        """
        self.Id = _id

        # Expression variables
        self.Budget = Y
        self.A = a
        self.B = b
        self.UtilityExpr = a * ln(Q) + b * ln(S) - a*ln(mu * e_rate * Q + 1)
        self.Price = p
        self.EcoCon = mu

        # Current period props
        self.CurrentPlan = 'Normal'  # plan defaults to normal delivery
        self.CurrentUtility = 0
        self.UtilityDisparity = 0

        # Friendship
        self.Friends = []
        self.Delta = delta
        self.Friend_Effect = None

        # History
        self.Qrecords = {}
        self.Srecords = {}
        self.PlanRecords = {}

        # ErrorLogger


    def EnterGenericRound(self, period, cG, cN, eG, eN, utility_handler):
        self.CurrentUtility = self.compare_generic(period, cG, cN, eG, eN, utility_handler)

    def compare_generic(self, period, cG, cN, eG, eN, utility_handler):
        # Eval utility for green delivery
        util_generic = utility_handler.Generic_Utility_Function.subs(
            [(S, utility_handler.Generic_Solved_S), (Q, utility_handler.Generic_Solved_Q)]      # Q,S subs (Q,S)
        )

        util_green, util_normal = self.evaluate_green_normal(util_generic, cG, cN, eG, eN)

        # compare utilities
        green_is_better = util_green > util_normal  # and util_green != util_normal  # I think this second operation is redundant

        if green_is_better:
            self.assign_green(util_green, util_normal, period, utility_handler, eG, cG)
            return util_green

        else:
            self.assign_normal(util_green, util_normal, period, utility_handler, eN, cN)
            return util_normal

    def assign_green(self, period, utility_handler, eG, cG):
        self.CurrentPlan = 'Green'
        #self.UtilityDisparity = util_green - util_normal
        self.PlanRecords[period] = 'Green'
        self.Qrecords[period] = utility_handler.Generic_Solved_Q.subs([(e_rate, eG),  # emissions subs (e_rate)
                                                                       (a, self.A), (b, self.B), (mu, self.EcoCon),
                                                                       # agent params subs (a,b,mu)
                                                                       (Y, self.Budget), (P, self.Price),
                                                                       (cGeneric, cG)]).evalf()  # budget subs (Y, P, cGeneric

        self.Srecords[period] = utility_handler.Generic_Solved_S.subs([(e_rate, eG),  # emissions subs (e_rate)
                                                                       (a, self.A), (b, self.B), (mu, self.EcoCon),
                                                                       # agent params subs (a,b,mu)
                                                                       (Y, self.Budget), (P, self.Price),
                                                                       (cGeneric, cG)]).evalf()  # budget subs (Y, P, cGeneric

    def assign_normal(self, period, utility_handler,eN,cN):
        self.CurrentPlan = 'Normal'
        #self.UtilityDisparity = util_normal - util_green
        self.PlanRecords[period] = 'Normal'
        self.Qrecords[period] = utility_handler.Generic_Solved_Q.subs([(e_rate, eN),  # emissions subs (e_rate)
                                                                       (a, self.A), (b, self.B), (mu, self.EcoCon),
                                                                       # agent params subs (a,b,mu)
                                                                       (Y, self.Budget), (P, self.Price),
                                                                       (cGeneric, cN)]).evalf()  # budget subs (Y, P, cGeneric
        self.Srecords[period] = utility_handler.Generic_Solved_S.subs([(e_rate, eN),  # emissions subs (e_rate)
                                                                       (a, self.A), (b, self.B), (mu, self.EcoCon),
                                                                       # agent params subs (a,b,mu)
                                                                       (Y, self.Budget), (P, self.Price),
                                                                       (cGeneric, cN)]).evalf()  # budget subs (Y, P, cGeneric

    def assign_green_social(self, period, utility_handler,eG,cG, friend_val):
        self.assign_green(period, utility_handler, eG, cG)
        self.Qrecords[period] = self.Qrecords[period].subs([(delta, self.Delta),(F,friend_val)])
        self.Srecords[period] = self.Srecords[period].subs([(delta, self.Delta),(F,friend_val)])

    def assign_normal_social(self, period, utility_handler, eN, cN, friend_val):
        self.assign_normal( period, utility_handler, eN, cN)
        self.Qrecords[period] = self.Qrecords[period].subs([(delta, self.Delta),(F,friend_val)])
        self.Srecords[period] = self.Srecords[period].subs([(delta, self.Delta),(F,friend_val)])


    def evaluate_green_normal(self, util_generic, cG, cN, eG, eN):
        util_green = util_generic.subs(
            [(e_rate, eG),                                                                      # emissions subs (e_rate)
             (a, self.A), (b, self.B), (mu, self.EcoCon),                                       # agent params subs (a,b,mu)
             (Y,self.Budget), (P, self.Price), (cGeneric, cG)]).evalf()                             # budget subs (Y, P, cGeneric


        util_normal = util_generic.subs(
            [(e_rate, eN),                                                                      # emissions subs (e_rate)
             (a, self.A), (b, self.B), (mu, self.EcoCon),                                       # agent params subs (a,b,mu)
             (Y,self.Budget), (P, self.Price), (cGeneric, cN)]).evalf()                              # budget subs (Y, P, cGeneric)

        return util_green,util_normal

    def evaluate_green_normal_social(self, util_generic, cG, cN, eG, eN, friends, period):
        generic_green, generic_normal = self.evaluate_green_normal(util_generic, cG, cN, eG, eN)
        util_green = generic_green.subs([
                                         (delta, self.Delta),
                                         (F,sum([1 for friend in friends if friend.PlanRecords[period - 1] == 'Green'])/len(friends))
                                        ]).evalf()
        util_normal = generic_normal.subs([
                                        (delta, self.Delta),
                                        (F, sum([1 for friend in friends if friend.PlanRecords[period - 1] == 'Normal'])/len(friends))
                                        ]).evalf()
        return util_green, util_normal

    def compare_generic_social(self,  period, cG, cN, eG, eN, friends, utility_handler):
        # Eval utility for green delivery
        util_generic = utility_handler.Generic_Utility_Function.subs(
            [(S, utility_handler.Generic_Solved_S), (Q, utility_handler.Generic_Solved_Q)]  # Q,S subs (Q,S)
        )

        util_green, util_normal = self.evaluate_green_normal_social(util_generic, cG, cN, eG, eN, friends, period)

        # compare utilities
        green_is_better = util_green > util_normal  # and util_green != util_normal  # I think this second operation is redundant

        if green_is_better:
            self.Friend_Effect = sum([1 for friend in friends if friend.PlanRecords[period - 1] == 'Green']) / len(friends)
            self.assign_green_social(period, utility_handler, eG, cG, self.Friend_Effect)
            return util_green

        else:
            self.Friend_Effect = sum([1 for friend in friends if friend.PlanRecords[period - 1] == 'Normal']) / len(friends)
            self.assign_normal_social(period, utility_handler, eN, cN,self.Friend_Effect)
            return util_normal


    def EnterRound(self, period, cG, cN, eG, eN):
        """
        At each period (round), the agent makes a decision between green and normal delivery using compare_plans().
        EnterRound() does not consider if an agent has any friends (use EnterSocialRound()).

        :param period: the iteration/ period that the Engine is in
        :param cG: consumption of green delivery
        :param cN: consumption of normal delivery
        :param eG: emissions of green delivery
        :param eN: emissions of normal delivery
        """
        self.CurrentUtility = self.compare_plans(period, cG, cN, eG, eN)

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

    def EnterBenchMarkRound(self, period, cN, eN, utility_handler):
        self.CurrentUtility = self.compare_normal_to_no_plan(period, cN, eN, utility_handler)

    def compare_normal_to_no_plan(self, period, cN, eN, utility_handler):
        util_generic = utility_handler.Generic_Utility_Function.subs(
            [(S, utility_handler.Generic_Solved_S), (Q, utility_handler.Generic_Solved_Q)]  # Q,S subs (Q,S)
        )
        util_normal = util_generic.subs(
            [(e_rate, eN),  # emissions subs (e_rate)
             (a, self.A), (b, self.B), (mu, self.EcoCon),  # agent params subs (a,b,mu)
             (Y, self.Budget), (P, self.Price), (cGeneric, cN)]).evalf()

        if util_normal > 0:
            self.assign_normal(period, utility_handler, eN, cN)
        else:
            self.CurrentPlan = 'None'
            # self.UtilityDisparity = util_normal - util_green
            self.PlanRecords[period] = 'None'
            self.Qrecords[period] = 0
            self.Srecords[period] = self.Budget


    def get_budget_expression(self, income, cost_of_plan):
        """
        The budget constraint is expressed in the form:
            B = Y - P*Q - S - cost_of_plan

        :param income: income forms part of the budget constraint
        :param cost_of_plan: cost of plan
        :return:
        """
        return income - P * Q - S - cost_of_plan

    def max_Q_and_S(self, utility_expr, budget, emissions, period):
        """
        Solve the optimisation problem that maximises Quantity consumed

        :param utility_expr:
        :param budget:
        :param emissions:
        :return:
        """
        L = utility_expr.subs(e_rate, emissions) - lam * (budget)  # L for the Lagrangian
        dQ = diff(L, Q)  # FOC 1
        dS = diff(L, S)  # FOC 2

        lam_sub = solve(dS, lam, simplify=False)[0]  # Get lamda to substitute into dQ and remove lamda from eq

        eq_to_solve = dQ.subs(lam, lam_sub)

        Q_in_terms_of_S = solve(eq_to_solve, Q, simplify=False)[0]

        # Solve with budget constraint to get S
        budget_in_terms_of_S = budget.subs(Q, Q_in_terms_of_S)

        # Subs P,mu,a,b
        numeric_budget_in_terms_of_S = budget_in_terms_of_S.subs(
            [(a, self.A), (b, self.B), (P, self.Price), (mu, self.EcoCon)])

        # solve S
        #S_sol = solve(numeric_budget_in_terms_of_S, S, simplify=False)
        #if not self.ErrorLogger.CheckSolutionExists(S_sol, period, self.Id):
         #   return (-1,-1)
        #S_sol = S_sol[0]
        S_sol = nsolve(numeric_budget_in_terms_of_S, 1)
        print(S_sol)


        Q_sol = Q_in_terms_of_S.subs([(a, self.A), (b, self.B), (P, self.Price), (mu, self.EcoCon), (S, S_sol)])


        return Q_sol, S_sol

    def compare_plans(self, period, cG, cN, eG, eN):
        """
        The agent evaluates and compares their expected utility for choosing green or normal utility.

        :param period:
        :param cG:
        :param cN:
        :param eG:
        :param eN:
        :return: the utility agent receives from which delivery plan they choose
        """
        # Eval utility for green delivery
        green_budget = self.get_budget_expression(self.Budget, cG)
        print(f"Maximising green for agent {self.Id} in period {period}")
        Q_sol_g, S_sol_g = self.max_Q_and_S(self.UtilityExpr, green_budget, eG, period)
        if Q_sol_g == -1 and S_sol_g == -1:
            return self.CurrentUtility

        util_green = self.UtilityExpr.subs(
            [(e_rate, eG), (a, self.A), (b, self.B), (P, self.Price), (mu, self.EcoCon), (S, S_sol_g), (Q, Q_sol_g)])

        # Eval utility for normal delivery
        normal_budget = self.get_budget_expression(self.Budget, cN)
        print(f"Maximising normal for agent {self.Id} in period {period}")
        Q_sol_n, S_sol_n = self.max_Q_and_S(self.UtilityExpr, normal_budget, eN, period)
        if Q_sol_n == -1 and S_sol_n == -1:
            return self.CurrentUtility

        # comment

        util_normal = self.UtilityExpr.subs(
            [(e_rate, eN), (a, self.A), (b, self.B), (P, self.Price), (mu, self.EcoCon), (S, S_sol_n), (Q, Q_sol_n)])

        # compare utilities
        green_is_better = util_green > util_normal  # and util_green != util_normal  # I think this second operation is redundant

        if green_is_better:
            self.CurrentPlan = 'Green'
            self.UtilityDisparity = util_green - util_normal
            self.Qrecords[period] = Q_sol_g
            self.Srecords[period] = S_sol_g
            self.PlanRecords[period] = 'Green'
            return util_green
        else:
            self.CurrentPlan = 'Normal'
            self.UtilityDisparity = util_normal - util_green
            self.Qrecords[period] = Q_sol_n
            self.Srecords[period] = S_sol_n
            self.PlanRecords[period] = 'Normal'
            return util_normal

    def compare_plans_social(self, period, cG, cN, eG, eN, friends):

        friend_emissions = sum(
            [eG * friend.Qrecords[period - 1] if friend.CurrentPlan == 'Green' else eN * friend.Qrecords[period - 1] for
             friend in friends])

        social_utility_expr = self.UtilityExpr + om * delta * ln(friend_emissions)

        # eval green utility
        green_budget = self.get_budget_expression(self.Budget, cG)

        Q_sol_g, S_sol_g = self.max_Q_and_S(social_utility_expr, green_budget, eG, period)

        util_green = social_utility_expr.subs(
            [(e_rate, eG), (om, self.Omega), (delta, self.Delta), (a, self.A), (b, self.B), (P, self.Price),
             (mu, self.EcoCon), (S, S_sol_g), (Q, Q_sol_g)])

        # eval normal utility
        normal_budget = self.get_budget_expression(self.Budget, cN)
        Q_sol_n, S_sol_n = self.max_Q_and_S(social_utility_expr, normal_budget, eN, period)

        util_normal = social_utility_expr.subs(
            [(e_rate, eN), (om, self.Omega), (delta, self.Delta), (a, self.A), (b, self.B), (P, self.Price),
             (mu, self.EcoCon), (S, S_sol_n), (Q, Q_sol_n)])

        # compare utilities
        green_is_better = util_green > util_normal and util_green != util_normal

        if green_is_better:
            self.CurrentPlan = 'Green'
            self.UtilityDisparity = util_green - util_normal
            return util_green
        else:
            self.CurrentPlan = 'Normal'
            self.UtilityDisparity = util_normal - util_green
            return util_normal

    def UpdateBudget(self,period):
        # subtract pay outs P*Q
        #self.Budget -= self.Price * self.Qrecords[period]
        # add savings
        self.Budget += self.Srecords[period]