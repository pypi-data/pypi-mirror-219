"""
Tools for processing math data. Either numerical result, some kind of numpy object or rendered string.
"""

import numpy as np


def magnitude(x: float) -> int:
    """
    calculate magnitude of given value

    Args:
        x (float): value

    Returns:
        Orders of magnitude in decimal system
    """
    return np.choose(
        x == 0,  # bool values, used as indices to the array
        [
            np.int_(np.log10(np.abs(x)) // 1),  # if false
            0,  # if true
        ],
    )


def chisquare(y_exp, y_obs, y_obs_error) -> float:
    """
    calculate chi square value: (y_expected - y_observed)^2 / delta_y_observed^2

    Args:
        y_exp: expected y-values
        y_obs: observed y-values
        y_obs_error: uncertainties of observed y-values

    Returns:
        chi square value
    """
    return sum(
        [
            (y_e - y) ** 2 / dy**2
            for y_e, y, dy in zip(y_exp, y_obs, y_obs_error, strict=True)
        ]
    )


def average(series) -> (float, float):
    """
    calculate average and standard error of average

    Args:
        series: Series of values

    Returns:
        average, standard error of average
    """
    return np.average(series), np.std(series, ddof=1) / np.sqrt(len(series))


def gaussian_fwhm(std: float, d_std: float) -> (float, float):
    """
    Calculate full width at half maximum of a gaussian.

    Args:
        std: standard derivation \\(\\sigma\\)
        d_std: error of standard derivation

    Returns:
        FWHM of gaussian
    """
    return 2 * np.sqrt(2 * np.log(2)) * std, 2 * np.sqrt(2 * np.log(2)) * d_std


def ls_minmax(data, num: int = 1000) -> np.ndarray:
    """
    returns linear spaced samples in the interval [min(data), max(data)] with length num=1000

    Args:
        data: series of data to gain min and max values
        num: number of samples

    Returns:
        linear spaced samples
    """
    return np.linspace(np.min(data), np.max(data), num)


def error_str(value: float, error: float, frmt: str = "plain", unit: str | None = None) -> str:
    """
    render value with uncertainty in string with right amount of decimal numbers in magnitude of value

    Args:
        value: value
        error: uncertainty of value
        frmt: format `plain`, `tex` or `si`
        unit: print unit behind value

    Returns:
        (value +- error)(e+-mag)
    """
    # todo implement siunitx format
    if magnitude(error) > magnitude(value):
        return ""
    mag_val = magnitude(value)
    mag_err = magnitude(error)
    decimals = mag_val - mag_err + 1
    val = value / 10.0**mag_val
    err = error / 10.0**mag_val

    if frmt == "si":  # TeX siunitx format
        return f"\\SI{{ {val} \\pm {err} e{mag_val} }}{{}}"

    string = "(" if (mag_val != 0) or (unit is not None) else ""
    string += f"{val:.{decimals}f} "
    string += r"\pm" if frmt == "tex" else "+-"
    string += f" {err:.{decimals}f}"
    string += ")" if mag_val != 0 or (unit is not None) else ""
    if (mag_val != 0) and (frmt == "tex"):
        string += f"10^{{{mag_val}}}"
    elif mag_val != 0:
        string += f"e{mag_val}"
    return string
