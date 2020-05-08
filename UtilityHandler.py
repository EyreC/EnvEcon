from EnvSymbols import *  # Also imports math and sympy

class UtilityHandler:
    def __init__(self):
        self.Generic_Utility_Function = a * ln(Q) + b * ln(S) - a * ln(mu * e_rate * Q + 1)
        self.Generic_Solved_Q = None
        self.Generic_Solved_S = None
        self.Generic_Budget_Expr = Y - P * Q - S - cGeneric


    def SolveNormal(self):
        Q_sol, S_sol = self.max_Q_and_S(self.Generic_Utility_Function)

        self.Generic_Solved_S = S_sol
        self.Generic_Solved_Q = Q_sol

    def SolveSocial(self):
        self.Generic_Utility_Function =  a * ln(Q) + b * ln(S) - a * ln(mu * e_rate * Q + 1) - a*delta*ln(1+F)

        Q_sol, S_sol = self.max_Q_and_S(self.Generic_Utility_Function)

        self.Generic_Solved_S = S_sol
        self.Generic_Solved_Q = Q_sol

    def max_Q_and_S(self, util_expr):
        L = util_expr - lam * (self.Generic_Budget_Expr)  # L for the Lagrangian
        dQ = diff(L, Q)  # FOC 1
        dS = diff(L, S)  # FOC 2

        lam_sub = solve(dS, lam, simplify=False)[0]  # Get lamda to substitute into dQ and remove lamda from eq

        eq_to_solve = dQ.subs(lam, lam_sub)

        Q_in_terms_of_S = solve(eq_to_solve, Q, simplify=False)[0]

        # Solve with budget constraint to get S
        budget_in_terms_of_S = self.Generic_Budget_Expr.subs(Q, Q_in_terms_of_S)

        S_sol = solve(budget_in_terms_of_S, S, simplify=False)[0]

        Q_sol = Q_in_terms_of_S.subs(S, S_sol)

        return Q_sol, S_sol