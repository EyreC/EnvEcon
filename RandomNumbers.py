def find_beta_shape_params(mode=0, concentration=0, mean=0, stdev=0, variance=0):

    if mean > 0 and (variance > 0 or stdev > 0):
        variance = variance if stdev==0 else stdev**2

        summa = (((1 - mean) * mean) / variance) - 1
        a = mean * summa
        b = (1 - mean) * summa
        return a, b

    elif mode > 0 and concentration > 0:
        a = (mode * (concentration - 2)) + 1
        b = ((1 - mode) * (concentration - 2)) + 1
        return a, b

    else:
        print("To find beta shape parameters, enter mode-concentration or mean-stdev/ mean-variance pairs."
              "The numbers must be positive.")


