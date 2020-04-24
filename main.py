from Engine import *

def main():

    print('Setting up')
    # Engine(self, num_agents, price, a_interval, mu_interval, income_interval,
    #        cG, cN, eG, eN,
    #        omega_interval=[0, 0], delta_interval=[0, 0], friend_interval=[0, 0])

    cN = 20
    cG = 5*cN  # Cost of green delivery shall be some multiplier ( >1) applied to cost of normal delivery

    engine = Engine(2, 3, [0.3, 0.7], [0.3, 0.6], [300, 500],
                    100, 20, 0.01, 0.03,
                    [0.3, 0.8], [0.3, 0.8], [1, 2])
    print('Finished engine set up')

    engine.RunNormal(1)  # run Normal for 1 iteration
    print('Finished')


if __name__ == '__main__':
    main()
