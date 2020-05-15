from Engine import *
from RandomNumbers import *

import copy


def main():

    # Shape parameters for beta distribution of alpha in utility function
    alpha_a, alpha_b = find_beta_shape_params(mean=0.2, stdev=0.04)

    # Shape parameters for lognormal distribution of income in utility function
    median_monthly_income = 22100 / 12
    log_income_mean = np.log(median_monthly_income)  # In a normal distribution, mean = median = mode.
    log_income_std = 0.4219793  # std of log-income of the bottom 97% of population

    # num_agents, price, a_interval, mu_interval, income_interval, cG, cN, eG, eN, inflation_rate,
    # delta_interval=[0, 0], friend_interval=[0, 0])

    engine = Engine(num_agents=20, price=12, a_interval=[alpha_a, alpha_b], mu_interval=[0.03, 0.06],
                    income_interval=[log_income_mean, log_income_std], cG=15, cN=8, eG=0.9, eN=1, inflation_rate=0.03,
                    delta_interval=[0.00003, 0.00005], friend_interval=[1, 2])
    # print('Starting normal rounds')

    cGs = range(15, 29, 5)  # Different prices
    for cG in cGs:
        periods = 5  # How many periods to be run

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

if __name__ == '__main__':
    main()
