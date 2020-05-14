from Engine import *
import time
from RandomNumbers import *

def main():
    mode, k = 0.75, 500  # mode and concentration

    # Shape parameters for beta distribution of alpha in utility function
    alpha_a, alpha_b = find_beta_shape_params(mean=0.4, stdev=0.05)

    #
    log_income_mean = np.log(22100) #22100
    log_income_std = 0.42198  # stdev of log-income of the bottom 97% of population


    print('Initialising engine')
    engine = Engine(50, 100, [alpha_a, alpha_b], [0.00003, 0.0006], [log_income_mean, log_income_std], 30, 20, 0.95, 1, 0.03,[0.00003, 0.00005], [1, 2])
    print('Starting normal rounds')
    engine.RunBenchMark(10)

if __name__ == '__main__':
    main()
