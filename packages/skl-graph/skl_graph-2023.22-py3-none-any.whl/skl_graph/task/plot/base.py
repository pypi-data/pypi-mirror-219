# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2018)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from typing import Callable

import numpy as nmpy
from matplotlib import pyplot as pypl
from mpl_toolkits.mplot3d import Axes3D as axes_3d_t

array_t = nmpy.ndarray

axes_t = pypl.Axes
axes_any_h = axes_t | axes_3d_t
figure_t = pypl.Figure

NewFigure = pypl.figure
EnterMatplotlibEventLoop = pypl.show

y_transform_h = Callable[[int | array_t], array_t]


def FigureAndAxesFromBoth(
    figure: figure_t | None, axes: axes_t | axes_3d_t | None, dimension: int, /
) -> tuple[figure_t, axes_any_h]:
    """"""
    if axes is None:
        if figure is None:
            figure = NewFigure()
        if dimension == 2:
            axes = figure.gca()
        else:
            axes = figure.add_subplot(1, 1, 1, projection=axes_3d_t.name)
        axes.invert_yaxis()
    else:
        figure = axes.get_figure()

    return figure, axes


def YTransformationsFromAxes(
    axes: axes_any_h, domain_height: int, /
) -> tuple[y_transform_h, y_transform_h]:
    """
    Note: For sites, an inverted y-axis (increasing to the bottom) is the normal, row/col convention for SKL-Graph, so
    TransformedY is the identity. However, it would flip vectors, so TransformedYForVector should indeed flip them.
    """
    # nmpy.asarray: To be able to transform several y's at once
    if axes.yaxis_inverted():
        TransformedY = lambda y: y
        TransformedYForVector = lambda y: -nmpy.asarray(y)
    else:
        max_0 = domain_height - 1
        TransformedY = lambda y: max_0 - nmpy.asarray(y)
        TransformedYForVector = lambda y: y

    return TransformedY, TransformedYForVector


def YTransformations(
    domain_height: int, /
) -> Callable[[axes_any_h], tuple[y_transform_h, y_transform_h]]:
    """"""
    return lambda _axs: YTransformationsFromAxes(_axs, domain_height)


def ManagePlotOptions(
    figure: figure_t,
    axes: axes_any_h,
    should_block: bool,
    should_return_figure: bool,
    should_return_axes: bool,
    /,
) -> figure_t | axes_t | axes_3d_t | tuple[figure_t, axes_any_h] | None:
    """"""
    # Preferably test not-axes_3d_t instead of yep-axes_t in case axes_3d_t is a subclass of axes_t
    if not isinstance(axes, axes_3d_t):
        # Matplotlib says: NotImplementedError: It is not currently possible to manually set the aspect on 3D axes
        axes.axis("equal")

    if should_block:
        EnterMatplotlibEventLoop()
        return None
    elif should_return_figure:
        if should_return_axes:
            return figure, axes
        else:
            return figure
    elif should_return_axes:
        return axes

    return None
