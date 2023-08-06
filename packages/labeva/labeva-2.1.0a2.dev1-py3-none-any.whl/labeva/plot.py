"""
Apply settings to matplotlib
"""

# %%
from datetime import datetime
from os import makedirs
from os import path

import matplotlib as mpl
import matplotlib.pyplot as plt


# %%
# === SETTINGS ===
PLOTTING = True
"""Enabe or disable plotting. to be used like `if PLOTTING: ...`"""
FASTRUN = False
"""Can be used to check whether to take smaller data sets to test code faster"""

# %%
FIGURE_SIZE = (10, 7)
"""MPL figure size"""
FIGURE_DPI = 300
"""MPL figure resolution"""
FIGURE_COLOR = "tab:blue"
"""Default color"""
FIGURE_CMAP = "gist_rainbow_r"
"""Default color map"""
FIGURE_SAVE = True
"""Whether `figure_save()` saves the figures"""
FIGURE_FORMAT = ""
"""File format used by `figure_save()` by default"""
FIGURE_DIR_SUBDIR = "fig"
"""Subdirectory of working directory to save figures in + timestamp (if not overwritten)"""
FIGURE_DIR_TIME = datetime.now()
"""Defaults to `datetime.now()`"""
FIGURE_DIR = path.join(
    FIGURE_DIR_SUBDIR, f"{FIGURE_DIR_TIME.strftime('%Y-%m-%dT%H-%M-%S')}"
)
"""Directory to save figures used by `figure_save()`"""
MPL_COLORS_TAB = [
    "tab:blue",
    "tab:green",
    "tab:orange",
    "tab:red",
    "tab:purple",
    "tab:pink",
    "tab:olive",
    "tab:cyan",
    "tab:gray",
    "tab:brown",
]
"""Set of MPL 'tab:' colors"""


# %%
# === PLOT SETTINGS ===
def figure_save(
    figure_name: str, dpi: int = FIGURE_DPI, fileformat: str = FIGURE_FORMAT
) -> None:
    """
    saves the current matplotlib figure to a file

    Args:
        figure_name: File name
        dpi: DPI of image file
        fileformat: Format of image file
    """
    dirname = FIGURE_DIR
    if FIGURE_SAVE and not FASTRUN:
        if not path.isdir(dirname):
            makedirs(dirname)
        return plt.savefig(
            path.join(
                dirname, figure_name + ("." if fileformat != "" else "") + fileformat
            ),
            dpi=dpi,
        )


save_figure = figure_save
"""aliase for `figure_save()`. legacy support, to be removed in a later version"""


# %%
def plt_setup(
    plotting: bool = None,
    size: (int, int) = None,
    dpi: int = None,
    cmap: str = None,
    save: bool = None,
    fileformat: str = None,
    dirname: str = None,
    dir_subdir: str = None,
    dir_time: str = None,
    fastrun: bool = None,
):
    """
    Sets up default matplotlib settings and changes by the module provided constants

    Args:
        plotting: whether to compute plots
        size: Size of mpl figures
        dpi: DPI of mpl figures
        cmap: color map
        save: whether to save mpl figures (effects `figure_save`)
        fileformat: Format of image file
        dirname: Directory to save image files to
        dir_subdir: Compute directory to save image files to with subdirectory name and timestamp (no effect if `dirname` is given)
        dir_time:
        fastrun:
    """
    global PLOTTING
    global FIGURE_SAVE
    global FASTRUN
    global FIGURE_SIZE
    global FIGURE_DPI
    global FIGURE_CMAP
    global FIGURE_SAVE
    global FIGURE_FORMAT
    global FIGURE_DIR
    global FIGURE_DIR_SUBDIR
    global FIGURE_DIR_TIME

    if plotting is not None:
        PLOTTING = plotting
    if fastrun is not None:
        FASTRUN = fastrun

    if size is not None:
        FIGURE_SIZE = size
    if dpi is not None:
        FIGURE_DPI = dpi
    if cmap is not None:
        FIGURE_CMAP = cmap
    if save is not None:
        FIGURE_SAVE = save
    if fileformat is not None:
        FIGURE_FORMAT = fileformat

    if dir_subdir is not None:
        FIGURE_DIR_SUBDIR = dir_subdir
    if dir_time is not None:
        FIGURE_DIR_TIME = dir_time

    if dirname is not None:
        FIGURE_DIR = dirname
    elif dir_subdir is not None:
        FIGURE_DIR = path.join(
            FIGURE_DIR_SUBDIR, f"{FIGURE_DIR_TIME.strftime('%Y-%m-%dT%H-%M-%S')}"
        )
    else:
        pass

    mpl.rcParams["figure.figsize"] = FIGURE_SIZE
    mpl.rcParams["figure.dpi"] = FIGURE_DPI

    # mpl.rcParams['text.latex.preamble'] = r"\usepackage{siunitx}"


# === PLOT LAYOUT ===
def args_err(
    *,
    ls: str = "",
    color: str = FIGURE_COLOR,
    marker: str = ".",
    mfc: str = FIGURE_COLOR,
    mec: str = "k",
    ms: int = 7,
    ecolor: str = "k",
    elinewidth: int = 2,
    capsize: int = 5,
    capthick: int = 2,
    **kwargs: str | int,
) -> dict[str, str | int]:
    """
    Provides (default) parameters for `plt.errorbar`. Can be used like
    ```python
    plt.errorbar(xdata, ydata, xerr=xerr, yerr=yerr, **args_err())
    ```
    If `None` is given, no value is set.

    Args:
        ls: line style
        color: line color
        marker: marker style
        mfc: marker face color
        mec: marker edge color
        ms: marker size
        ecolor: error bar color
        elinewidth: error bar line width
        capsize: error bar cap size
        capthick: error bar cap thickness
        **kwargs: other valid `plt.errorbar` parameters can be provided

    Returns:
        Dictionary with parameters
    """
    dct = {}
    for key, value in locals().values():
        if value is not None:
            dct[key] = value
    return dct


def args_plt(
    *, ls: str = "dashed", color: str = FIGURE_COLOR, **kwargs: str | int
) -> dict[str, str | int]:
    """
    Provides (default) parameters for `plt.plot`. Can be used like
    ```python
    plt.plot(xdata, ydata, **args_plot())
    ```
    If `None` is given, no value is set.

    Args:
        ls: line style
        color: line color
        **kwargs: other valid `plt.plot` parameters can be provided

    Returns:
        Dictionary with parameters
    """
    dct = {}
    for key, value in locals().values():
        if value is not None:
            dct[key] = value
    return dct
