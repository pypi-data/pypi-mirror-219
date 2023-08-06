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

from typing import Iterable

import networkx as ntkx
import numpy as nmpy
from matplotlib.collections import PatchCollection as patch_2d_collection_t
from matplotlib.patches import Rectangle as rectangle_t
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as poly_3d_collection_t

from skl_graph.task.plot.base import axes_3d_t, axes_t, y_transform_h
from skl_graph.type.graph import skl_graph_t
from skl_graph.type.node import array_t, branch_node_t, end_node_t, node_t
from skl_graph.type.style import label_style_t, node_styles_h

# Note: these array_t's are one-element arrays, so the type should be tuple[int, ...] if it were not for not wasting
# time with .item()'s in the elements of TransformedPosition.
positions_as_dict_h = dict[str, tuple[array_t, ...]]


_CUBE = [
    [[-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5]],
    [[-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, -0.5, -0.5]],
    [[0.5, -0.5, 0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [0.5, 0.5, 0.5]],
    [[-0.5, -0.5, 0.5], [-0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5]],
    [[-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, -0.5]],
    [[-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5]],
]
_CUBE = nmpy.array(_CUBE)
_CUBE_TRANSPARENCY = 0.6


def PositionsForPlotFromDetails(
    details: Iterable[tuple[str, node_t]], TransformedY: y_transform_h, /
) -> positions_as_dict_h:
    """"""
    TransformedPosition = lambda _psn: (_psn[1], TransformedY(_psn[0]), *_psn[2:])

    return dict((_uid, TransformedPosition(_dtl.position)) for _uid, _dtl in details)


def Plot2DEndNodes(
    nodes: Iterable[tuple[str, node_t]],
    TransformedY: y_transform_h,
    axes: axes_t,
    node_styles: node_styles_h,
    /,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    style_set = set(node_styles.keys())
    squares_and_styles = [
        (
            rectangle_t(
                (_dtl.position[1] - 0.5, TransformedY(_dtl.position[0]) - 0.5), 1, 1
            ),
            style_set.intersection(_dtl.properties.keys()),
        )
        for _, _dtl in nodes
        if isinstance(_dtl, end_node_t)
    ]

    if squares_and_styles.__len__() > 0:
        squares, custom_styles = zip(*squares_and_styles)
        degree_based_color = node_styles.get(1, node_styles[None]).color
        node_colors = tuple(
            _sty.pop().color if _sty.__len__() > 0 else degree_based_color
            for _sty in custom_styles
        )
        if set(node_colors).__len__() > 1:
            for square, color in zip(squares, node_colors):
                square.set_facecolor(color)
                axes.add_patch(square)
        else:
            collection = patch_2d_collection_t(squares, facecolor=node_colors[0])
            axes.add_collection(collection)


def Plot3DEndNodes(
    nodes: Iterable[tuple[str, node_t]],
    TransformedY: y_transform_h,
    axes: axes_3d_t,
    node_styles: node_styles_h,
    /,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    style_set = set(node_styles.keys())
    cubes_and_styles = [
        (
            nmpy.add(
                _CUBE,
                (_dtl.position[1], TransformedY(_dtl.position[0]), _dtl.position[2]),
            ),
            style_set.intersection(_dtl.properties.keys()),
        )
        for _, _dtl in nodes
        if isinstance(_dtl, end_node_t)
    ]

    if cubes_and_styles.__len__() > 0:
        cubes, custom_styles = zip(*cubes_and_styles)
        degree_based_color = node_styles.get(1, node_styles[None]).color
        node_colors = tuple(
            _sty.pop().color if _sty.__len__() > 0 else degree_based_color
            for _sty in custom_styles
        )
        if set(node_colors).__len__() > 1:
            for cube, color in zip(cubes, node_colors):
                cube.set_facecolor(color)
                cube.set_alpha(_CUBE_TRANSPARENCY)
                axes.add_patch(cube)
        else:
            collection = poly_3d_collection_t(
                nmpy.concatenate(cubes),
                facecolor=node_colors[0],
                alpha=_CUBE_TRANSPARENCY,
            )
            axes.add_collection3d(collection)


def Plot2DBranchNodes(
    nodes: Iterable[tuple[str, node_t]],
    degrees: dict[str, int],
    TransformedY: y_transform_h,
    axes: axes_t,
    node_styles: node_styles_h,
    /,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    default_style = node_styles[None]
    style_set = set(node_styles.keys())
    for uid, details in nodes:
        if isinstance(details, branch_node_t):
            custom_style = style_set.intersection(details.properties.keys())
            if custom_style.__len__() > 0:
                node_style = custom_style.pop()
            else:
                node_style = degrees[uid]
            node_style = node_styles.get(node_style, default_style)

            corners_0 = details.sites[1] - 0.5
            corners_1 = TransformedY(details.sites[0]) - 0.5
            squares = [
                rectangle_t(corner, 1, 1) for corner in zip(corners_0, corners_1)
            ]

            collection = patch_2d_collection_t(squares, facecolor=node_style.color)
            axes.add_collection(collection)


def Plot3DBranchNodes(
    nodes: Iterable[tuple[str, node_t]],
    degrees: dict[str, int],
    TransformedY: y_transform_h,
    axes: axes_3d_t,
    node_styles: node_styles_h,
    /,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    default_style = node_styles[None]
    style_set = set(node_styles.keys())
    for uid, details in nodes:
        if isinstance(details, branch_node_t):
            custom_style = style_set.intersection(details.properties.keys())
            if custom_style.__len__() > 0:
                node_style = custom_style.pop()
            else:
                node_style = degrees[uid]
            node_style = node_styles.get(node_style, default_style)

            corners_0 = details.sites[1] - 0.5
            corners_1 = TransformedY(details.sites[0]) - 0.5
            corners_2 = details.sites[2] - 0.5
            cubes = [
                nmpy.add(_CUBE, corner)
                for corner in zip(corners_0, corners_1, corners_2)
            ]

            collection = poly_3d_collection_t(
                nmpy.concatenate(cubes),
                facecolor=node_style.color,
                alpha=_CUBE_TRANSPARENCY,
            )
            axes.add_collection3d(collection)


def Plot2DNodeLabels(
    skl_graph: skl_graph_t,
    node_label_positions: positions_as_dict_h,
    axes: axes_t,
    /,
) -> None:
    """"""
    # NetworkX changes axes styles. Save here to set back afterward.
    axes_styles = {}
    for axis, name in ((axes.xaxis, "x"), (axes.yaxis, "y")):
        axes_styles[name] = {}
        for level in ("minor", "major"):
            axes_styles[name][level] = axis.get_tick_params(which=level)

    ntkx.draw_networkx_labels(
        skl_graph,
        ax=axes,
        pos=node_label_positions,
        font_size=int(round(skl_graph.label_styles[0].size)),
        font_color=skl_graph.label_styles[0].color,
    )

    for name, styles in axes_styles.items():
        for level, style in styles.items():
            axes.tick_params(
                axis=name,
                which=level,
                **style,
            )


def Plot3DNodeLabels(
    nodes: Iterable[str],
    positions_as_dict: positions_as_dict_h,
    axes: axes_3d_t,
    style: label_style_t,
    /,
) -> None:
    """"""
    for node in nodes:
        axes.text(
            *positions_as_dict[node], node, fontsize=style.size, color=style.color
        )
