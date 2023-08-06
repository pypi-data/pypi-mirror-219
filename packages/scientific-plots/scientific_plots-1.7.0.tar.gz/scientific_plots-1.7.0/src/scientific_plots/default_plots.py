#!/usr/bin/env Python3
# pylint: disable=too-many-locals,too-many-arguments
"""
This module contains a few functions, which can be used to
generate plots quickly and with useful defaults"""
from __future__ import annotations
from pathlib import Path
from functools import wraps
from typing import TypeVar, List, Tuple, Union, Callable, Optional
from warnings import warn, filterwarnings, catch_warnings
from textwrap import dedent

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from numpy import amin, amax

from .plot_settings import apply_styles, rwth_cycle
from .types_ import Vector, Matrix

mpl.use("Agg")

In = TypeVar("In", List[float], Tuple[float],
             Vector)

In2D = TypeVar("In2D", list[list[float]], list[Vector], tuple[Vector],
               Matrix)


def fix_inputs(input_1: In, input_2: In)\
        -> tuple[Vector, Vector]:
    """
    Remove nans and infinities from the input vectors.

    Parameters
    ---------
    input_1, input_2:
        X/Y-axis data of plot

    Returns
    ------
    New vectors x and y with nans removed.
    """
    if len(input_1) != len(input_2):
        raise ValueError(
            "The sizes of the input vectors are not the same.")
    nan_count = np.count_nonzero(np.isnan(input_2))
    inf_count = np.count_nonzero(np.isinf(input_2))
    if nan_count != 0 or inf_count != 0:
        new_input_1 = np.empty(len(input_1)-nan_count-inf_count)
        new_input_2 = np.empty(len(new_input_1))
        position = 0
        for x_input, y_input in zip(input_1, input_2):
            if not np.isnan(y_input) or np.isinf(y_input):
                new_input_1[position] = x_input
                new_input_2[position] = y_input
                position += 1
        return new_input_1, new_input_2

    return np.array(input_1), np.array(input_2)


def check_inputs(input_1: In, input_2: In, label_1: str, label_2: str)\
        -> bool:
    """
    Check the input vectors to see, if they are large enough.

    Parameters
    ---------
    input_1, input_2:
        X/Y-axis data of plot

    label_1, label_2:
        Labels of the X/Y axis

    Returns
    ------
    True, if the plot can be created.
    """
    if len(input_1) <= 1 or len(input_2) <= 1:
        warn(
            "There are not enough points in the following plots:"
            f"label1: {label_1} label2: {label_2}. It cannot be drawn.")
        return False

    if min(input_1) == max(input_1):
        warn(
            "The area of the x-axis is not large enough in the following plot:"
            f"label1: {label_1} label2: {label_2}. It cannot be drawn.")
        return False

    if min(input_2) == max(input_2):
        warn(
            "The area of the y-axis is not large enough in the following plot:"
            f"label1: {label_1} label2: {label_2}. It cannot be drawn.")
        return False

    infinity = np.isinf(input_1).any() or np.isinf(input_2).any()
    if infinity:
        warn(dedent(f"""There are infinities in the data of the following plot:
             label1: {label_1}, label2: {label_2}. It cannot be drawn."""),
             RuntimeWarning)
        return False

    nan = np.isnan(input_1).any() or np.isnan(input_2).any()
    if nan:
        warn(dedent(f"""There are nans in the data of the following plot:
             label1: {label_1}, label2: {label_2}. It cannot be drawn."""),
             RuntimeWarning)
        return False

    return True


@apply_styles
def plot_fit(X: In, Y: In,
             fit_function: Callable[..., float],
             xlabel: str, ylabel: str, filename: Union[str, Path], *,
             args: Optional[Tuple[float]] = None,
             logscale: bool = False) -> None:
    """Creates a plot of data and a fit and saves it to 'filename'."""
    X, Y = fix_inputs(X, Y)  # type: ignore
    if not check_inputs(
            X, Y, xlabel, ylabel):
        return

    n_fit = 1000

    _fit_function: Callable[[float], float]
    if args is not None:

        @wraps(fit_function)
        def _fit_function(x: float) -> float:
            """This is the function, which has been fitted"""
            return _fit_function(x, *args)
    else:
        _fit_function = fit_function

    plt.plot(X, Y, label="data")
    X_fit = [min(X) + (max(X) - min(X)) * i / (n_fit - 1)
             for i in range(n_fit)]
    Y_fit = [_fit_function(x) for x in X_fit]
    plt.plot(X_fit, Y_fit, label="fit")
    if logscale:
        plt.xscale("log")
        plt.yscale("log")
    plt.xlim(min(X), max(X))
    if logscale:
        plt.ylim(min(Y) * 0.97, max(Y) * 1.02)
    else:
        plt.ylim(
            min(Y) - (max(Y) - min(Y)) * 0.02,
            max(Y) + (max(Y) - min(Y)) * 0.02
        )
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


@apply_styles(three_d=True)
def plot_surface(X: In2D, Y: In2D, Z: In2D,
                 xlabel: str, ylabel: str, zlabel: str,
                 filename: Union[str, Path], *,
                 log_scale: bool = False,
                 set_z_lim: bool = True,
                 colorscheme: str = "rwth_gradient",
                 figsize: tuple[float, float] = (4.33, 3.5),
                 labelpad: Optional[float] = None,
                 nbins: Optional[int] = None) -> None:
    """create a 2D surface plot of meshgrid-like valued Xs, Ys and Zs"""
    if not check_inputs(
            np.array(X).flatten(),
            np.array(Z).flatten(), xlabel, zlabel):
        return
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    fig.subplots_adjust(left=-0.02, right=0.75, bottom=0.15, top=0.98)
    ax.plot_surface(X, Y, Z, cmap=colorscheme)
    ax.set_box_aspect(aspect=None, zoom=.8)

    if labelpad is None:
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel, rotation=90)
    else:
        ax.set_xlabel(xlabel, labelpad=labelpad)
        ax.set_ylabel(ylabel, labelpad=labelpad)
        ax.set_zlabel(zlabel, rotation=90, labelpad=labelpad)

    assert ax.zaxis is not None

    ax.set_xlim(amin(X), amax(X))  # type: ignore
    ax.set_ylim(amin(Y), amax(Y))  # type: ignore

    if set_z_lim:
        if not log_scale:
            ax.set_zlim(
                amin(Z) - (amax(Z) - amin(Z)) * 0.02,  # type: ignore
                amax(Z) + (amax(Z) - amin(Z)) * 0.02  # type: ignore
            )
        else:
            ax.set_zlim(
                amin(Z) * 0.97, amax(Z) * 1.02)  # type: ignore

    if log_scale:
        ax.set_yscale("log")
        ax.set_xscale("log")
        ax.set_zscale("log")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.xaxis.pane.set_alpha(0.3)
    ax.yaxis.pane.set_alpha(0.3)
    ax.zaxis.pane.set_alpha(0.3)

    if nbins is not None:
        ax.xaxis.set_major_locator(
            MaxNLocator(nbins)
        )
        ax.yaxis.set_major_locator(
            MaxNLocator(nbins)
        )

    fig.set_size_inches(*figsize)

    with catch_warnings():
        filterwarnings("ignore", message=".*Tight layout")
        plt.tight_layout()
        plt.savefig(filename)

    plt.close()


@apply_styles
def plot(X: In, Y: In, xlabel: str, ylabel: str,
         filename: Union[Path, str], *, logscale: bool = False,
         ylim: Optional[tuple[float, float]] = None,
         yticks: bool = True, cycler: int = 0) -> None:
    """Create a simple 1D plot"""
    X, Y = fix_inputs(X, Y)  # type: ignore
    if not check_inputs(
            X, Y, xlabel, ylabel):
        return
    if len(X) <= 1 or len(Y) <= 1:
        raise ValueError(
            f"The data for plot {filename} contains empty rows!")

    if cycler > 0:
        for _ in range(cycler):
            plt.plot([], [])
    plt.plot(X, Y, linestyle="-")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if logscale:
        plt.xscale("log")
        plt.yscale("log")
        if ylim is None:
            plt.ylim(min(Y) * 0.97, max(Y) * 1.02)
    elif ylim is None:
        plt.ylim(
            min(Y) - (max(Y) - min(Y)) * 0.02,
            max(Y) + (max(Y) - min(Y)) * 0.02
        )
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlim(min(X), max(X))
    if not yticks:
        plt.yticks([])
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


@apply_styles
def two_plots(x1: In, y1: In, label1: str,
              x2: In, y2: In, label2: str,
              xlabel: str, ylabel: str,
              filename: Union[Path, str], *,
              logscale: bool = False, cycle: int = 0,
              color: tuple[int, int] = (0, 1),
              outer: bool = False) -> None:
    """Create a simple 1D plot with two different graphs inside of a single
    plot and a single y-axis.

    Keyword arguments:
    cycle -- skip this many colours in the colour-wheel before plotting
    color -- use these indeces in the colour-wheel when creating a plot
    outer -- use the outer limits on the x-axis rather than the inner limit
    """
    x1, y1 = fix_inputs(x1, y1)  # type: ignore
    x2, y2 = fix_inputs(x2, y2)  # type: ignore

    if not (
            check_inputs(x1, y1, xlabel, label1)
            or check_inputs(x2, y2, xlabel, label2)):
        return
    if len(x1) <= 1 or len(y1) <= 1 or len(y2) <= 1 or len(x2) <= 1:
        raise ValueError(
            f"The data for plot {filename} contains empty rows!")

    if cycle > 0:
        color = (color[0] + cycle, color[1] + cycle)

    # access colour
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    try:
        linestyle = prop_cycle.by_key()["linestyle"]
    except KeyError:
        linestyle = rwth_cycle.by_key()["linestyle"]
    colors = prop_cycle.by_key()["color"]

    if max(color) >= len(colors):
        colors += colors
        linestyle += linestyle

    plt.plot(x1, y1, label=label1,
             color=colors[color[0]],
             linestyle=linestyle[0])

    plt.plot(x2, y2, label=label2,
             color=colors[color[1]],
             linestyle=linestyle[1])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    min_ = min(min(y1), min(y2))
    max_ = max(max(y1), max(y2))
    if not logscale:
        plt.ylim(
            min_ - (max_ - min_) * 0.02,
            max_ + (max_ - min_) * 0.02
        )
    else:
        plt.xscale("log")
        plt.yscale("log")
        plt.ylim(
            min_ * 0.97, max_ * 1.02)

    if outer:
        plt.xlim(min(min(x1), min(x2)),
                 max(max(x1), max(x2)))
    else:
        plt.xlim(max(min(x1), min(x2)),
                 min(max(x1), max(x2)))

    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


@apply_styles
def three_plots(x1: In, y1: In, label1: str,
                x2: In, y2: In, label2: str,
                x3: In, y3: In, label3: str,
                xlabel: str, ylabel: str,
                filename: Union[Path, str], *,
                logscale: bool = False,
                xmin: Optional[float] = None,
                xmax: Optional[float] = None) -> None:
    """Create a simple 1D plot with three different graphs inside of a single
    plot and a single y-axis."""
    x1, y1 = fix_inputs(x1, y1)  # type: ignore
    x2, y2 = fix_inputs(x2, y2)  # type: ignore
    x3, y3 = fix_inputs(x3, y3)  # type: ignore
    if not (
            check_inputs(x1, y1, xlabel, label1)
            or check_inputs(x2, y3, xlabel, label1)
            or check_inputs(x3, y3, xlabel, label3)):
        return

    if any(len(x) <= 1 for x in (x1, x2, y1, y2, x3, y3)):
        raise ValueError(
            f"The data for plot {filename} contains empty rows!")

    plt.plot(x1, y1, label=label1)
    plt.plot(x2, y2, label=label2, linestyle="dashed")
    plt.plot(x3, y3, label=label3, linestyle="dotted")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    min_ = min(min(y1), min(y2), min(y3))
    max_ = max(max(y1), max(y2), max(y3))
    if not logscale:
        plt.ylim(
            min_ - (max_ - min_) * 0.02,
            max_ + (max_ - min_) * 0.02
        )
    else:
        plt.xscale("log")
        plt.yscale("log")
        plt.ylim(
            min_ * 0.97, max_ * 1.02)
    if xmin is not None and xmax is not None:
        plt.xlim(xmin, xmax)
    else:
        plt.xlim(min(x1), max(x1))
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


@apply_styles
def two_axis_plots(x1: In, y1: In, label1: str,
                   x2: In, y2: In, label2: str,
                   xlabel: str, ylabel: str,
                   ylabel2: str,
                   filename: Union[Path, str], *,
                   ticks: Optional[tuple[list[float], list[str]]] = None,
                   xlim: Optional[tuple[float, float]] = None,
                   color: tuple[int, int] = (0, 1))\
        -> None:
    """Create a simple 1D plot with two different graphs inside of a single
    plot with two y-axis.
    The variable "ticks" sets costum y-ticks on the second y-axis. The first
    argument gives the position of the ticks and the second argument gives the
    values to be shown.
    Color selects the indeces of the chosen color-wheel, which should be taken
    for the different plots. The default is (1,2)."""
    x1, y1 = fix_inputs(x1, y1)  # type: ignore
    x2, y2 = fix_inputs(x2, y2)  # type: ignore
    if not check_inputs(
            y1, y2, label1, label2):
        return
    if len(x1) <= 1 or len(y1) <= 1 or len(y2) <= 1 or len(x2) <= 1:
        raise ValueError(
            f"The data for plot {filename} contains empty rows!")

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # access colour
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    try:
        linestyle = prop_cycle.by_key()["linestyle"]
    except KeyError:
        linestyle = rwth_cycle.by_key()["linestyle"]
    colors = prop_cycle.by_key()["color"]

    if max(color) >= len(colors):
        colors += colors
        linestyle += linestyle

    # first plot
    lines = ax1.plot(x1, y1, label=label1,
                     color=colors[color[0]],
                     linestyle=linestyle[0])
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_ylim(
        min(y1) - (max(y1) - min(y1)) * 0.02,
        max(y1) + (max(y1) - min(y1)) * 0.02
    )

    # second plot
    ax2 = ax1.twinx()
    lines += ax2.plot(x2, y2, label=label2,
                      color=colors[color[1]],
                      linestyle=linestyle[1])
    ax2.set_ylabel(ylabel2)
    ax2.set_ylim(
        min(y2) - (max(y2) - min(y2)) * 0.02,
        max(y2) + (max(y2) - min(y2)) * 0.02
    )

    # general settings
    if xlim is None:
        plt.xlim(min(x1), max(x1))
    else:
        plt.xlim(*xlim)
    labels = [line.get_label() for line in lines]
    plt.legend(lines, labels)
    # ticks
    if ticks is not None:
        ax2.set_yticks(ticks[0])
        ax2.set_yticklabels(ticks[1])
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def make_invisible(ax: plt.Axes) -> None:
    """Make all patch spines invisible."""
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for spine in ax.spines.values():
        spine.set_visible(False)


@apply_styles
def three_axis_plots(x1: In, y1: In, label1: str,
                     x2: In, y2: In, label2: str,
                     x3: In, y3: In, label3: str,
                     xlabel: str, ylabel: str,
                     ylabel2: str, ylabel3: str,
                     filename: Union[Path, str], *,
                     ticks: Optional[tuple[list[float], list[str]]] = None,
                     xlim: Optional[tuple[float, float]] = None,
                     color: tuple[int, int, int] = (0, 1, 2),
                     legend: bool = True)\
        -> None:
    """Create a simple 1D plot with two different graphs inside of a single
    plot with two y-axis.
    The variable "ticks" sets costum y-ticks on the second y-axis. The first
    argument gives the position of the ticks and the second argument gives the
    values to be shown.
    Color selects the indeces of the chosen color-wheel, which should be taken
    for the different plots. The default is (1,2)."""
    # pylint: disable=R0915
    x1, y1 = fix_inputs(x1, y1)  # type: ignore
    x2, y2 = fix_inputs(x2, y2)  # type: ignore
    x3, y3 = fix_inputs(x3, y3)  # type: ignore
    if not check_inputs(
            y1, y2, label1, label2):
        return
    if not check_inputs(
            x3, y3, xlabel, label3):
        return

    if len(x1) <= 1 or len(y1) <= 1 or len(y2) <= 1 or len(x2) <= 1:
        raise ValueError(
            f"The data for plot {filename} contains empty rows!")
    assert len(color) == 3

    fig, ax1 = plt.subplots()
    fig.subplots_adjust(right=0.75)
    # access colour
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    try:
        linestyle = prop_cycle.by_key()["linestyle"]
    except KeyError:
        linestyle = rwth_cycle.by_key()["linestyle"]
    colors = prop_cycle.by_key()["color"]

    if max(color) >= len(colors):
        colors += colors
        linestyle += linestyle

    # first plot
    lines = ax1.plot(x1, y1, label=label1,
                     color=colors[color[0]],
                     linestyle=linestyle[0])
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_ylim(
        min(y1) - (max(y1) - min(y1)) * 0.02,
        max(y1) + (max(y1) - min(y1)) * 0.02
    )
    ax1.yaxis.label.set_color(colors[color[0]])
    ax1.tick_params(axis="y", colors=colors[color[0]])

    # second plot
    ax2 = ax1.twinx()
    lines += ax2.plot(x2, y2, label=label2,
                      color=colors[color[1]],
                      linestyle=linestyle[1])
    ax2.set_ylabel(ylabel2)
    ax2.set_ylim(
        min(y2) - (max(y2) - min(y2)) * 0.02,
        max(y2) + (max(y2) - min(y2)) * 0.02
    )
    ax2.yaxis.label.set_color(colors[color[1]])
    ax2.tick_params(axis="y", colors=colors[color[1]])

    # third plot
    ax3 = ax1.twinx()
    make_invisible(ax3)
    ax3.spines["right"].set_position(("axes", 1.25))
    ax3.spines["right"].set_visible(True)
    lines += ax3.plot(x3, y3, label=label3,
                      color=colors[color[2]],
                      linestyle=linestyle[2])
    ax3.set_ylabel(ylabel3)
    ax3.set_ylim(
        min(y3) - (max(y3) - min(y3)) * 0.02,
        max(y3) + (max(y3) - min(y3)) * 0.02
    )
    ax3.yaxis.label.set_color(colors[color[2]])
    ax3.tick_params(axis="y", colors=colors[color[2]])

    # general settings
    if xlim is None:
        plt.xlim(min(x1), max(x1))
    else:
        plt.xlim(*xlim)
    labels = [line.get_label() for line in lines]
    if legend:
        plt.legend(lines, labels)
    # ticks
    if ticks is not None:
        ax2.set_yticks(ticks[0])
        ax2.set_yticklabels(ticks[1])
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
