import os
import matplotlib.pylab as plt

__all__ = [
    "save_plt",
    "load_default_plot_settings",
    "load_default_plot_settings_02",
]


def save_plt(n, rdir="", vect="pdf,eps"):
    """Save plot in the required formats

    Parameters
    ----------
    n : str
        plot name
    rdir : str, optional
        directory, by default ''
    vect : str, optional
        vectory formats, leave empty to save only png, by default "pdf,eps"
    """
    if os.path.exists(os.path.dirname(rdir)):
        for vect_ in vect.split(","):
            if vect_ == "pdf" or vect_ == "eps":
                plt.savefig(os.path.join(rdir, "%s.%s" % (n, vect_)))
        plt.savefig(os.path.join(rdir, "%s.png" % (n)), dpi=300)
    else:
        print("Figure NOT saved, directory doesn't exist")
    return


def load_default_plot_settings(grid_bool=True):
    """Load default plot settings"""
    params = {
        "figure.figsize": (10, 6),
        "savefig.bbox": "tight",
        "axes.grid": grid_bool,
        "errorbar.capsize": 3,
        "axes.titlesize": 16,
        "axes.labelsize": 16,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "legend.fontsize": 14,
    }
    plt.rcParams.update(params)


def load_default_plot_settings_02(grid_bool=True):
    """Load default plot settings"""
    params = {
        "figure.figsize": (10, 6),
        "savefig.bbox": "tight",
        "axes.grid": grid_bool,
        "errorbar.capsize": 3,
        "axes.titlesize": 24,
        "axes.labelsize": 24,
        "xtick.labelsize": 26,
        "ytick.labelsize": 26,
        "legend.fontsize": 26,
    }
    plt.rcParams.update(params)
