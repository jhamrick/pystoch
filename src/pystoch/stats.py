import numpy as np
import scipy.stats

def kolmogorov_smirnov(samples, name, params, num_boot=1000):
    idx = np.random.randint(np.array(samples).size, size=(num_boot, np.array(samples).size))
    bootsamps = np.array(samples)[idx]
    Ds = np.zeros(num_boot)
    p_values = np.zeros(num_boot)

    for i in xrange(bootsamps.shape[0]):
        D, p_value = scipy.stats.kstest(bootsamps[i], name, params)
        Ds[i] = D
        p_values[i] = p_value

    D = np.round(np.mean(Ds), decimals=3)
    D_err = np.round(scipy.stats.sem(Ds), decimals=4)

    return D, D_err
