#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py:

This file runs the main program. It accepts
"""

from Engine import *
from RandomNumbers import *

import copy


@timer
def main():
    
    # Engine inputs
    num_agents = 1000  # ETA 90-100 seconds
    price_of_average_good = 65
    alpha_mean, alpha_std = 0.2, 0.04  
    mu_mean, mu_std = 0.07, 0.03
    median_monthly_income = 22100 / 12  
    log_income_std = 0.4219793
    price_of_normal_delivery = 8
    emissions_of_green_delivery = 0.9  
    emissions_of_normal_delivery = 1
    inflation_rate = 0.017

    # Calculations for distribution shape parameters
    alpha_a, alpha_b = find_beta_shape_params(mean=alpha_mean, stdev=alpha_std)
    mu_a, mu_b = find_beta_shape_params(mean=mu_mean, stdev=mu_std)
    log_income_mean = np.log(median_monthly_income)  # In a normal distribution, mean = median = mode.

    # Initiate engine with input values
    engine = Engine(num_agents=num_agents, price=price_of_average_good, a_params=[alpha_a, alpha_b],
                    mu_params=[mu_a, mu_b], income_interval=[log_income_mean, log_income_std],
                    cG=0, cN=price_of_normal_delivery, eG=emissions_of_green_delivery, eN=emissions_of_normal_delivery, 
                    inflation_rate=inflation_rate, delta_interval=[0.01, 0.1], friend_interval=[1, 10])


    # Running simulations
    prices_of_green_delivery = range(15, 31, 3)  # At what different prices of green delivery do you want to simulate?
    periods = 24  # How many periods for each simulation to be ran?

    for i in range(50): # How many times do you want the simulation to be ran? (monte carlo)
        for cG in prices_of_green_delivery:


            engine_copy = copy.deepcopy(engine)
            engine_copy.cG = cG
            engine_copy.AggregationManager.cG = cG
            engine_copy.RunBenchMark(periods)

            engine_copy = copy.deepcopy(engine)
            engine_copy.cG = cG
            engine_copy.AggregationManager.cG = cG
            engine_copy.RunNormal(periods)

            engine_copy = copy.deepcopy(engine)
            engine_copy.cG = cG
            engine_copy.AggregationManager.cG = cG
            engine_copy.RunSocial(periods)

    print(f"\n{len(prices_of_green_delivery) * 3} simulations ran overall, reflecting the following prices of green "
          f"delivery: {[i for i in prices_of_green_delivery]}.\n"
          f"Number of agents: {num_agents}\n"
          f"Median monthly income: {round(median_monthly_income, 2)}\n"
          f"Price of average good: {price_of_average_good}\n"
          f"Alpha average (stdev): {round(alpha_mean, 2)} ({round(alpha_std, 2)})\n"
          f"Eco consciousness average (stdev): {round(mu_mean, 3)} ({round(mu_std, 3)})")


if __name__ == '__main__':
    main()
