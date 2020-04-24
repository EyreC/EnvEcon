from EnvSymbols import *


class Agent:

    def __init__(self, _id, a, b, mu, Y, p, omega=0, delta=0, friends=[]):
        """
        Initialises an Agent object with the following attributes:

        :param _id: unique identifier
        :param a: preference for consumption (coefficient of ln[Q])
        :param b: preference for savings (coefficient of ln[S])
        :param mu: eco-consicousness
        :param Y: income
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
        self.UtilityExpr = a * ln(Q) + b * ln(S) - ln(mu * e_rate * Q + 1)
        self.Price = p
        self.EcoCon = mu

        # Current period props
        self.CurrentPlan = 'Normal'  # plan defaults to normal delivery
        self.CurrentUtility = 0
        self.UtilityDisparity = 0

        # Friendship
        self.Friends = []
        self.Omega = omega
        self.Delta = delta

        # History
        self.Qrecords = {}
        self.Srecords = {}
        self.PlanRecords = {}

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

    def EnterSocialRound(self, period, cG, cN, eG, eN, friends):
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
        self.CurrentUtility = self.compare_plans_social(period, cG, cN, eG, eN, friends)

    def get_budget_expression(self, income, cost_of_plan):
        return income - P * Q - S - cost_of_plan

    def max_Q_and_S(self, utility_expr, budget, emissions):
        """
        Solve the optimisation problem that maximises Quantity consumed

        :param utility_expr:
        :param budget:
        :param emissions:
        :return:
        """
        L = utility_expr.subs(e_rate, emissions) - lam * (budget)
        dQ = diff(L, Q)  # FOC 1

        dS = diff(L, S)  # FOC 2

        lam_sub = solve(dS, lam)[0]  # get lamda to substitute into dQ and remove lamda from eq

        eq_to_solve = dQ.subs(lam, lam_sub)

        Q_in_terms_of_S = solve(eq_to_solve, Q)[0]

        # Solve with budget constraint to get S
        budget_in_terms_of_S = budget.subs(Q, Q_in_terms_of_S)

        # Subs P,mu,a,b
        numeric_budget_in_terms_of_S = budget_in_terms_of_S.subs(
            [(a, self.A), (b, self.B), (P, self.Price), (mu, self.EcoCon)])

        # solve S
        S_sol = solve(numeric_budget_in_terms_of_S, S)[0]

        Q_sol = Q_in_terms_of_S.subs([(a, self.A), (b, self.B), (P, self.Price), (mu, self.EcoCon), (S, S_sol)])

        return Q_sol, S_sol

    def compare_plans(self, period, cG, cN, eG, eN):
        # eval utility for green delivery
        green_budget = self.get_budget_expression(self.Budget, cG)
        print(f"Maximising green for agent {self.Id} in period {period}")
        Q_sol_g, S_sol_g = self.max_Q_and_S(self.UtilityExpr, green_budget, eG)

        util_green = self.UtilityExpr.subs(
            [(e_rate, eG), (a, self.A), (b, self.B), (P, self.Price), (mu, self.EcoCon), (S, S_sol_g), (Q, Q_sol_g)])

        # eval utility for normal delivery
        normal_budget = self.get_budget_expression(self.Budget, cN)
        print(f"Maximising normal for agent {self.Id} in period {period}")
        Q_sol_n, S_sol_n = self.max_Q_and_S(self.UtilityExpr, normal_budget, eN)
        # comment

        util_normal = self.UtilityExpr.subs(
            [(e_rate, eN), (a, self.A), (b, self.B), (P, self.Price), (mu, self.EcoCon), (S, S_sol_n), (Q, Q_sol_n)])

        # compare utilities
        green_is_better = util_green > util_normal and util_green != util_normal

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

        Q_sol_g, S_sol_g = self.max_Q_and_S(social_utility_expr, green_budget, eG)

        util_green = social_utility_expr.subs(
            [(e_rate, eG), (om, self.Omega), (delta, self.Delta), (a, self.A), (b, self.B), (P, self.Price),
             (mu, self.EcoCon), (S, S_sol_g), (Q, Q_sol_g)])

        # eval normal utility
        normal_budget = self.get_budget_expression(self.Budget, cN)
        Q_sol_n, S_sol_n = self.max_Q_and_S(social_utility_expr, normal_budget, eN)

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
