import copy

from Engine import *
import time
from RandomNumbers import *


def main():

    # Shape parameters for beta distribution of alpha in utility function
    alpha_a, alpha_b = find_beta_shape_params(mean=0.2, stdev=0.04)

    mean_annual_income = 22100
    mean_monthly_income = mean_annual_income / 12
    log_income_mean = np.log(mean_monthly_income)
    log_income_std = 0.4219793  # stdev of log-income of the bottom 97% of population

    print('Initialising engine')
    # num_agents, price, a_interval, mu_interval, income_interval, cG, cN, eG, eN, delta_interval=[0, 0],
    # friend_interval=[0, 0])
    engine = Engine(10, 1, [alpha_a, alpha_b], [0.3, 0.6], [log_income_mean, log_income_std], 15, 8, 0.95, 1, 0.03,
                    [0.00003, 0.00005], [1, 2])
    # print('Starting normal rounds')

    cGs = range(15, 31, 10)
    for cG in cGs:
        itr = 2

        engine_copy = copy.deepcopy(engine)
        engine_copy.cG = cG
        engine_copy.AggregationManager.cG = cG
        print('Running benchmark')
        engine_copy.RunBenchMark(itr)

        engine_copy = copy.deepcopy(engine)
        engine_copy.cG = cG
        engine_copy.AggregationManager.cG = cG
        print('Running normal')
        engine_copy.RunNormal(itr)

        engine_copy = copy.deepcopy(engine)
        engine_copy.cG = cG
        engine_copy.AggregationManager.cG = cG
        print('Running social')
        engine_copy.RunSocial(itr)

if __name__ == '__main__':
    main()
