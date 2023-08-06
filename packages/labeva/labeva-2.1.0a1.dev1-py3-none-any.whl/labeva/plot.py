# %%
from datetime import datetime
from os import makedirs
from os import path

import matplotlib as mpl
import matplotlib.pyplot as plt


# %%
# === SETTINGS ===
PLOTTING = True
FASTRUN = False

# %%
FIGURE_SIZE = (10, 7)
FIGURE_DPI = 300
FIGURE_CMAP = "gist_rainbow_r"
FIGURE_SAVE = True
FIGURE_FORMATE = ""
FIGURE_DIR_SUBDIR = "fig"
FIGURE_DIR_TIME = datetime.now()
FIGURE_DIR = path.join(
    FIGURE_DIR_SUBDIR, f"{FIGURE_DIR_TIME.strftime('%Y-%m-%dT%H-%M-%S')}"
)


# %%
# === PLOT SETTINGS ===
def figure_save(figure_name, dpi=FIGURE_DPI, formate=FIGURE_FORMATE):
    dirname = FIGURE_DIR
    if FIGURE_SAVE and not FASTRUN:
        if not path.isdir(dirname):
            makedirs(dirname)
        return plt.savefig(
            path.join(dirname, figure_name + ("." if formate != "" else "") + formate),
            dpi=dpi,
        )


save_figure = figure_save  # legacy support, to be removed in a later version


# %%
def plt_setup(
    plotting=None,
    size=None,
    dpi=None,
    cmap=None,
    save=None,
    formate=None,
    dirname=None,
    dir_subdir=None,
    dir_time=None,
    fastrun=None,
):
    global PLOTTING
    global FIGURE_SAVE
    global FASTRUN
    global FIGURE_SIZE
    global FIGURE_DPI
    global FIGURE_CMAP
    global FIGURE_SAVE
    global FIGURE_FORMATE
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
    if formate is not None:
        FIGURE_FORMATE = formate

    if dir_subdir is not None:
        FIGURE_DIR_SUBDIR = dir_subdir
    if dir_time is not None:
        FIGURE_DIR_TIME = dir_time

    if dirname is None:
        FIGURE_DIR = path.join(
            FIGURE_DIR_SUBDIR, f"{FIGURE_DIR_TIME.strftime('%Y-%m-%dT%H-%M-%S')}"
        )
    else:
        FIGURE_DIR = dirname

    mpl.rcParams["figure.figsize"] = FIGURE_SIZE
    mpl.rcParams["figure.dpi"] = FIGURE_DPI

    # mpl.rcParams['text.latex.preamble'] = r"\usepackage{siunitx}"


# === PLOT LAYOUT ===
def args_err(
    *,
    ls="",
    marker=".",
    mfc="blue",
    mec="k",
    ms=7,
    ecolor="k",
    elinewidth=2,
    capsize=5,
    capthick=2,
    **kwargs,
):
    dct = {}
    for key, value in locals().values():
        if value is not None:
            dct[key] = value
    return dct


def args_plt(*, ls="dashed", color="blue", **kwargs):
    dct = {}
    for key, value in locals().values():
        if value is not None:
            dct[key] = value
    return dct
