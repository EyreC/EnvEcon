from Engine import *

def main():
    mode, k = 0.75, 500  # mode and concentration

    beta_distribution_a = (mode * (k - 2)) + 1
    beta_distribution_b = ((1 - mode) * (k - 2)) + 1


    print('Initialising engine')
    engine = Engine(10, 3, [0.3, 0.7], [0.3, 0.6], [300, 500], 30, 20, 0.95, 1, [0.00003, 0.00005], [1, 2])
    print('Starting normal rounds')
    engine.RunSocial(2)

if __name__ == '__main__':
    main()
