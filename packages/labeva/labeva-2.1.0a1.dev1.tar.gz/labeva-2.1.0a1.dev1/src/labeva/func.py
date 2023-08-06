import numpy as np


def lin(x, m, b):
    return m * x + b


def quad(x, a, x0, y0):
    return a * (x - x0) ** 2 + y0


def polynom(x, *args):
    return sum([args[i] * x**i for i in range(len(args))])


def exp(x, k, a, b):
    return a * np.exp(k * x) + b


def exp_decay(t, tau, a, b):
    return a * np.exp(-t / tau) + b


def ln(x, tau, b, a):
    return tau * np.log((x - b) / a)  # tau = 1/k from expfunc


# statistical distributions
def gauss(x, x0, std, a0, b):
    return a0 * np.exp(-((x - x0) ** 2) / (2 * std**2)) + b


def gauss_normalized(x, x0, std):
    return gauss(x, x0, std, 1 / (std * np.sqrt(2 * np.pi)), 0)
