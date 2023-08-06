#!/usr/bin/env python3
"""
This module contains the settings for the various plots.
Plots can be created using the 'figure' deocorator from this module.
Multiple plots for various cases will be created and saved to
the hard drive
"""
from __future__ import annotations

import csv
import locale
from contextlib import contextmanager
from copy import copy, deepcopy
from functools import wraps
from typing import (
    Generator, Optional, Union, Callable, Any, overload)
from pathlib import Path
from warnings import warn, catch_warnings, simplefilter
from textwrap import dedent

import mpl_toolkits
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
from matplotlib import colors
from cycler import cycler
import numpy as np

from .utilities import translate
from .types_ import Vector

mpl.use("Agg")
plt.rcParams["axes.unicode_minus"] = False

SPINE_COLOR = "black"
FIGSIZE = (4.4, 3.0)
FIGSIZE_SMALL = (2.2, 2.1)
_savefig = copy(plt.savefig)  # backup the old save-function


def linestyles() -> Generator[str, None, None]:
    """get the line-stiles as an iterator"""
    yield "-"
    yield "dotted"
    yield "--"
    yield "-."


rwth_colorlist: list[tuple[int, int, int]] = [(0, 84, 159), (246, 168, 0),
                                              (161, 16, 53), (0, 97, 101)]
rwth_cmap = colors.ListedColormap(rwth_colorlist, name="rwth_list")
mpl.colormaps.register(rwth_cmap)

rwth_hex_colors = ["#00549F", "#F6A800", "#A11035", "#006165",
                   "#57AB27", "#E30066"]

rwth_cycle = (
    cycler(color=rwth_hex_colors)
    + cycler(linestyle=["-", "--", "-.", "dotted",
                        (0, (3, 1, 1, 1, 1, 1)),
                        (0, (3, 5, 1, 5))]))

rwth_gradient: dict[str, tuple[tuple[float, float, float],
                               tuple[float, float, float]]] = {
    "red": ((0.0, 0.0, 0.0), (1.0, 142 / 255, 142 / 255)),
    "green": ((0.0, 84 / 255.0, 84 / 255), (1.0, 186 / 255, 186 / 255)),
    "blue": ((0.0, 159 / 255, 159 / 255), (1.0, 229 / 255, 229 / 255)),
}


def make_colormap(seq: list[tuple[tuple[Optional[float], ...],
                                  float,
                                  tuple[Optional[float], ...]]],
                  name: str = "rwth_gradient")\
        -> colors.LinearSegmentedColormap:
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    cdict: dict[str, list[tuple[float,
                                Optional[float],
                                Optional[float]
                                ]
                          ]] =\
        {"red": [], "green": [], "blue": []}
    for item in seq:
        red_1, green_1, blue_1 = item[0]
        red_2, green_2, blue_2 = item[2]

        cdict["red"].append((item[1], red_1, red_2))
        cdict["green"].append((item[1], green_1, green_2))
        cdict["blue"].append((item[1], blue_1, blue_2))
    return colors.LinearSegmentedColormap(name, cdict)


def partial_rgb(*x: float) -> tuple[float, ...]:
    """return the rgb value as a fraction of 1"""
    return tuple(v / 255.0 for v in x)


hks_44 = partial_rgb(0.0, 84.0, 159.0)
hks_44_75 = partial_rgb(64.0, 127.0, 183.0)
rwth_orange = partial_rgb(246.0, 168.0, 0.0)
rwth_orange_75 = partial_rgb(250.0, 190.0, 80.0)
rwth_gelb = partial_rgb(255.0, 237.0, 0.0)
rwth_magenta = partial_rgb(227.0, 0.0, 102.0)
rwth_bordeux = partial_rgb(161.0, 16.0, 53.0)


rwth_gradient_map = make_colormap(
    [
        ((None, None, None), 0., hks_44),
        (hks_44_75, 0.33, hks_44_75),
        (rwth_orange_75, 0.66, rwth_orange),
        (rwth_bordeux, 1., (None, None, None))
    ]
)
mpl.colormaps.register(rwth_gradient_map)


def _germanify(ax: Axes, reverse: bool = False) -> None:
    """
    translate a figure from english to german.
    The direction can be reversed, if reverse it set to True
    Use the decorator instead
    """

    for axi in ax.figure.axes:
        try:
            axi.ticklabel_format(
                useLocale=True)
        except AttributeError:
            pass
        items = [
            axi.xaxis.label,
            axi.yaxis.label,
            *axi.get_xticklabels(),
            *axi.get_yticklabels(),
        ]
        try:
            if axi.zaxis is not None:
                items.append(axi.zaxis.label)
                items += [*axi.get_zticklabels()]
        except AttributeError:
            pass
        if axi.get_legend():
            items += [*axi.get_legend().texts]
        for item in items:
            item.set_text(translate(item.get_text(),
                                    reverse=reverse))
    try:
        plt.tight_layout()
    except IndexError:
        pass


@contextmanager
def germanify(ax: Axes,
              reverse: bool = False) -> Generator[None, None, None]:
    """
    Translate the plot to german and reverse
    the translation in the other direction. If reverse is set to false, no
    reversal of the translation will be applied.
    """
    old_locale = locale.getlocale(locale.LC_NUMERIC)
    try:
        try:
            locale.setlocale(locale.LC_ALL, "de_DE")
            locale.setlocale(locale.LC_NUMERIC, "de_DE")
        except locale.Error:
            # locale not available
            pass
        plt.rcParams["axes.formatter.use_locale"] = True
        _germanify(ax)
        yield
    except Exception as e:
        print("Translation of the plot has failed")
        print(e)
        raise
    finally:
        try:
            locale.setlocale(locale.LC_ALL, old_locale)
            locale.setlocale(locale.LC_ALL, old_locale)
        except locale.Error:
            pass
        plt.rcParams["axes.formatter.use_locale"] = False
        if reverse:
            _germanify(ax, reverse=True)


def data_plot(filename: Union[str, Path]) -> None:
    """
    Write the data, which is to be plotted, into a txt-file in csv-format.
    """
    # pylint: disable=W0613
    if isinstance(filename, str):
        file_ = Path(filename)
    else:
        file_ = filename
    file_ = file_.parent / (file_.stem + ".csv")
    ax = plt.gca()
    try:
        with open(file_, "w", encoding="utf-8", newline="") as data_file:
            writer = csv.writer(data_file)
            for line in ax.get_lines():
                writer.writerow(
                    [line.get_label(), ax.get_ylabel(), ax.get_xlabel()])
                writer.writerow(line.get_xdata())
                writer.writerow(line.get_ydata())
    except PermissionError as e:
        print(f"Data-file could not be written for {filename}.")
        print(e)


def read_data_plot(filename: Union[str, Path])\
        -> dict[str, tuple[Vector, Vector]]:
    """Read and parse the csv-data-files, which have been generated by the
    'data_plot'-function."""
    data: dict[str, tuple[Vector, Vector]] = {}
    with open(filename, "r", newline="", encoding="utf-8") as file_:
        reader = csv.reader(file_)
        title: str
        x_data: Vector
        for i, row in enumerate(reader):
            if i % 3 == 0:
                title = row[0]
            elif i % 3 == 1:
                x_data = np.array(row, dtype=float)
            else:
                y_data: Vector
                y_data = np.array(row, dtype=float)
                data[title] = (x_data, y_data)
    return data


@contextmanager
def presentation_figure(figsize: tuple[float, float] = (4, 3)) ->\
        Generator[Axes, None, None]:
    """context manager to open an close the file.
    default seaborn-like plot"""
    fig, ax = plt.subplots(figsize=figsize)
    mpl.rcParams["text.latex.preamble"] = [
        r"\usepackage{helvet}",  # set the normal font here
        r"\usepackage{sansmath}",  # load up the sansmath so that math
        # -> helvet
        r"\sansmath",  # <- tricky! -- gotta actually tell tex to use!
    ]
    mpl.rc("font", family="sans-serif")
    mpl.rc("text", usetex=True)
    font = {"size": 30}

    mpl.rc("font", **font)
    plt.set_cmap("rwth_list")
    try:
        yield ax
    except Exception as e:
        print("creation of plot failed")
        print(e)
        raise
    finally:
        plt.close(fig)
        plt.close("all")
        mpl.rcParams.update(mpl.rcParamsDefault)
        plt.style.use("default")


old_save = plt.savefig


def try_save(filename: Path,
             dpi: Optional[int] = None,
             bbox_inches: Optional[Union[str, tuple[float, float]]] = None, *,
             small: bool = False) -> None:
    """Try to save the current figure to the given path, if it is not possible,
    try to save it under a different name.
    If small is set to true, also create
    a smaller version of the given plot."""
    try:
        old_save(filename, dpi=dpi, bbox_inches=bbox_inches)
    except PermissionError:
        old_save(filename.parent / (filename.stem + "_" + filename.suffix),
                 dpi=dpi, bbox_inches=bbox_inches)

    if small:
        fig = deepcopy(plt.gcf())
        fig.set_size_inches(*FIGSIZE_SMALL)
        with catch_warnings(record=True) as warning:
            simplefilter("always")
            fig.tight_layout()
            if warning:
                if issubclass(warning[-1].category, UserWarning):
                    plt.close(fig)
                    return
        folder = filename.parent / "small"
        folder.mkdir(exist_ok=True)
        try:
            fig.savefig(
                folder
                / filename.name, dpi=dpi, bbox_inches=bbox_inches)
        except PermissionError:
            fig.savefig(
                folder
                / (filename.stem + "_" + filename.suffix),
                dpi=dpi, bbox_inches=bbox_inches)
        plt.close(fig)


def new_save_simple(subfolder: Union[str, Path] = "", suffix: str = "", *,
                    german: bool = False, png: bool = True,
                    pdf: bool = True, small: bool = False)\
        -> Callable[..., None]:
    """
    Return a new save function, which saves the file to a new given name in pdf
    format, and also creates a png version.
    If the argument "german" is set to true, also create German language
    version of the plots.
    """

    @wraps(old_save)
    def savefig_(filename: Union[Path, str],
                 dpi: Optional[int] = None,
                 bbox_inches: Optional[
                     Union[tuple[float, float], str]] = None) -> None:
        """Save the plot to this location as pdf and png."""
        if isinstance(filename, str):
            filename = Path(filename)
        if filename.parent == Path("."):
            warn(
                f"The filename {filename} in 'savefig' does "
                f"not contain a subfolder (i.e. 'subfolder/{filename})! "
                "Many files might be created onto the top level.")

        if subfolder:
            (filename.parent / subfolder).mkdir(exist_ok=True)
            new_path_pdf = filename.parent / subfolder / (
                filename.stem + suffix + ".pdf")
            new_path_png = filename.parent / subfolder / (
                filename.stem + suffix + ".png")
        else:
            new_path_pdf = filename.parent / (
                filename.stem + suffix + ".pdf")
            new_path_png = filename.parent / (
                filename.stem + suffix + ".png")

        # save the data
        data_path = filename.parent / (
            filename.stem + ".dat")

        if not data_path.exists():
            data_plot(data_path)

        try:
            plt.tight_layout()
        except IndexError:
            pass
        # save the figure
        if pdf:
            try_save(new_path_pdf, bbox_inches=bbox_inches, small=small)
        if png:
            try_save(new_path_png, bbox_inches=bbox_inches,
                     dpi=dpi, small=small)

        if german:
            with germanify(plt.gca()):
                if pdf:
                    try_save(
                        new_path_pdf.parent
                        / (new_path_pdf.stem + "_german.pdf"),
                        bbox_inches=bbox_inches, small=small)
                if png:
                    try_save(
                        new_path_png.parent
                        / (new_path_png.stem + "_german.png"),
                        bbox_inches=bbox_inches, dpi=dpi, small=small)

    return savefig_


def presentation_settings() -> None:
    """Change the settings of rcParams for presentations."""
    # increase size
    fig = plt.gcf()
    fig.set_size_inches(8, 6)
    mpl.rcParams["font.size"] = 24
    mpl.rcParams["axes.titlesize"] = 24
    mpl.rcParams["axes.labelsize"] = 24
    # mpl.rcParams["axes.location"] = "left"
    mpl.rcParams["lines.linewidth"] = 3
    mpl.rcParams["lines.markersize"] = 10
    mpl.rcParams["xtick.labelsize"] = 18
    mpl.rcParams["ytick.labelsize"] = 18
    mpl.rcParams["figure.figsize"] = (10, 6)
    mpl.rcParams["figure.titlesize"] = 24

    mpl.rcParams["font.family"] = "sans-serif"


def set_rwth_colors(three_d: bool = False) -> None:
    """Apply the RWTH CD colors to matplotlib."""
    mpl.rcParams["text.usetex"] = False
    mpl.rcParams["axes.prop_cycle"] = rwth_cycle
    if three_d:
        plt.set_cmap("rwth_gradient")
    else:
        plt.set_cmap("rwth_list")


def set_serif() -> None:
    """Set the plot to use a style with serifs."""
    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["font.serif"] = [
        "cmr10", "stix", "Times New Roman"]


def set_sans_serif() -> None:
    """Set matplotlib to use a sans-serif font."""
    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["font.sans-serif"] = [
        "Arial", "Helvetica", "DejaVu Sans"]


class ThreeDPlotException(Exception):
    """This exception is called when a 3D plot is drawn. This is used to exit
    the plotting function with the science-style."""


def check_3d(three_d: bool) -> None:
    """This function checks if the current plot is a 3d plot. In that case, an
    exception is thrown, which can be used to stop the creation of the default
    plot."""
    if three_d:
        raise ThreeDPlotException
    if isinstance(plt.gca(), mpl_toolkits.mplot3d.axes3d.Axes3D):
        raise ThreeDPlotException


PlotFunction = Callable[..., None]


@overload
def apply_styles(plot_function: PlotFunction, *,
                 three_d: bool = False) -> PlotFunction:
    ...


@overload
def apply_styles(plot_function: None, *, three_d: bool = False)\
        -> Callable[[PlotFunction], PlotFunction]:
    ...


@overload
def apply_styles(*, three_d: bool = False)\
        -> Callable[[PlotFunction], PlotFunction]:
    ...


def apply_styles(plot_function: Optional[PlotFunction] = None, *,
                 three_d: bool = False)\
        -> Union[Callable[[PlotFunction], PlotFunction], PlotFunction]:
    """Apply the newly defined styles to a function, which creates a plot."""
    # pylint: disable=too-many-statements

    def _decorator(_plot_function: PlotFunction) -> PlotFunction:
        """This is the  actual decorator. Thus, the outer function
        'apply_styles' is actually a decorator-factory."""

        @wraps(_plot_function)
        def new_plot_function(*args: Any, **kwargs: Any) -> None:
            """
            New plotting function, with applied styles.
            """
            # default plot
            plt.set_cmap("rwth_list")
            plt.savefig = new_save_simple()
            _plot_function(*args, **kwargs)

            errors = (OSError, FileNotFoundError, ThreeDPlotException)

            def journal() -> None:
                """Create a plot for journals."""
                set_rwth_colors(three_d)
                set_serif()
                plt.savefig = new_save_simple("journal", png=False,
                                              small=not three_d)
                _plot_function(*args, **kwargs)

            def sans_serif() -> None:
                """
                Create a plot for journals with sans-serif-fonts.
                """
                set_rwth_colors(three_d)
                set_sans_serif()
                plt.savefig = new_save_simple("sans_serif", german=True,
                                              small=not three_d)
                _plot_function(*args, **kwargs)

            def grayscale() -> None:
                """
                Create a plot in grayscales for disserations.
                """
                mpl.rcParams["text.usetex"] = False
                set_serif()
                if three_d:
                    plt.set_cmap("Greys")
                    new_kwargs = copy(kwargs)
                    new_kwargs["colorscheme"] = "Greys"
                else:
                    new_kwargs = kwargs
                plt.savefig = new_save_simple("grayscale", png=False,
                                              small=not three_d)
                _plot_function(*args, **new_kwargs)

            def presentation() -> None:
                """
                Create a plot for presentations.
                """
                if three_d:
                    new_kwargs = copy(kwargs)
                    new_kwargs["figsize"] = (9, 7)
                    new_kwargs["labelpad"] = 20
                    new_kwargs["nbins"] = 5
                else:
                    new_kwargs = kwargs
                set_rwth_colors(three_d)
                presentation_settings()
                set_sans_serif()
                plt.savefig = new_save_simple("presentation",
                                              german=True, pdf=False)
                _plot_function(*args, **new_kwargs)

            try:
                check_3d(three_d)

                # test if this context is available
                plt.close("all")

                # journal
                with plt.style.context(["science", "ieee"]):
                    journal()

                # sans-serif
                with plt.style.context(["science", "ieee", "nature"]):
                    sans_serif()

                # grayscale
                with plt.style.context(["science", "ieee", "grayscale"]):
                    grayscale()

                # presentation
                with plt.style.context(["science", "ieee"]):
                    presentation()

            except errors:
                if not three_d:
                    warn(dedent(""""Could not found style 'science'.
                                The package was probably installed incorrectly.
                                Using a fallback-style."""), ImportWarning)
                # journal
                with plt.style.context("fast"):
                    if not three_d:
                        mpl.rcParams["figure.figsize"] = FIGSIZE
                        mpl.rcParams["font.size"] = 10
                    journal()

                # sans-serif
                with plt.style.context("fast"):
                    if not three_d:
                        mpl.rcParams["figure.figsize"] = FIGSIZE
                        mpl.rcParams["font.size"] = 10
                    sans_serif()

                # grayscale
                with plt.style.context("grayscale"):
                    if not three_d:
                        mpl.rcParams["figure.figsize"] = FIGSIZE
                        mpl.rcParams["font.size"] = 10
                    grayscale()

                # presentation
                with plt.style.context("fast"):
                    presentation()

            plt.savefig = old_save

        return new_plot_function

    if plot_function is not None:
        return _decorator(plot_function)

    return _decorator
