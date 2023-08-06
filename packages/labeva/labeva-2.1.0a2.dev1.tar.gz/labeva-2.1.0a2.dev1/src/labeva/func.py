"""
Provide common functions like a linear function \\(m * x + b\\).
"""

import numpy as np


def lin(x, m, b):
    """
    linear function
    
    Args:
        x: x
        m: slope
        b: y-offset
    """
    return m * x + b


def quad(x, a, x0, y0):
    """
    Parabel function
    
    Args:
        x: x
        a: stretching factor
        x0: x-offset
        y0: y-offset
    """
    return a * (x - x0) ** 2 + y0


def polynom(x, *args):
    """
    Polynomial function with arbitrary order
    \\( y = a_0 x + a_1 x + a_2 x + \\dots \\)
    
    Args:
        x: x
        *args: \\(a_i\\)
    """
    return sum([args[i] * x**i for i in range(len(args))])


def exp(x, k, a, b):
    """
    Exponential function
    \\( y = a \\times \\exp(k \\times x) + b \\)
    
    Args:
        x: x
        k: grow rate
        a: Start value
        b: y-offset
    """
    return a * np.exp(k * x) + b


def exp_decay(t, tau, a, b):
    """
    Exponential function
    \\( y = a \\times \\exp(\\tau \\times t) + b \\)
    
    Args:
        t: t
        tau: decay time
        a: Start value
        b: y-offset
    """
    return a * np.exp(-t / tau) + b


def ln(x, tau, a, b):
    """
    logarithmic function
    \\( y = \\tau \\times \\ln\\left(\\frac{x - b}{a}\\right) \\)
    inverse of exponential function with \\(\\tau = 1/k_{exp}\\)
    
    Args:
        x: x
        tau: stretching factor
        a: Start value of exp
        b: y-offset of exp
    """
    return tau * np.log((x - b) / a)  # tau = 1/k from expfunc


# statistical distributions
def gauss(x, x0, std, a0, b):
    """
    Gaussian distribution
    
    Args:
        x: x
        x0: expected value \\(\\mu\\)
        std: standard derivation \\(\\sigma\\)
        a0: Peak height
        b: y-offset
    """
    return a0 * np.exp(-((x - x0) ** 2) / (2 * std**2)) + b


def gauss_normalized(x, x0, std):
    """
    Normalized gaussian distribution
    
    Args:
        x: x
        x0: expected value \\(\\mu\\)
        std: standard derivation \\(\\sigma\\)
    """
    return gauss(x, x0, std, 1 / (std * np.sqrt(2 * np.pi)), 0)
