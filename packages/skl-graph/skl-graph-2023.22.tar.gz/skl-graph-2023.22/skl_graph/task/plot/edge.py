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

import numpy as nmpy

from skl_graph.feature.edge import InwardEndTangents
from skl_graph.task.plot.base import axes_t, y_transform_h
from skl_graph.type.edge import edge_t
from skl_graph.type.style import (
    direction_style_t,
    edge_styles_h,
    label_style_t,
    plot_mode_e,
)

_SUBSAMPLING_FACTOR = 0.75
_LABEL_BBOX_STYLE = {
    "facecolor": "w",
    "linestyle": "",
    "alpha": 0.5,
    "boxstyle": "square,pad=0",
}


def Plot(
    edges: Iterable[tuple[str, str, str, edge_t]],
    TransformedY: y_transform_h,
    TransformedYForVector: y_transform_h,
    axes: axes_t,
    edge_styles: edge_styles_h,
    direction_style: direction_style_t,
    label_style: label_style_t,
    mode: plot_mode_e,
    /,
) -> None:
    """"""
    # space_dim = edges[0][2].dim  # Does not work since 'MultiEdgeDataView' object is not subscriptable
    space_dim = 2
    for *_, details in edges:
        space_dim = details.dim
        break

    PlotEdge = axes.plot if space_dim == 2 else axes.plot3D
    PlotEdgeLabel = axes.text

    for source, target, uid, details in edges:
        if mode is plot_mode_e.SKL_Curve:
            as_curve = details.AsCurve()
            if as_curve is None:
                sites = list(details.sites)
            else:
                max_arc_length = as_curve.x.item(-1)
                n_samples = int(round(_SUBSAMPLING_FACTOR * details.lengths.length))
                arc_lengths = nmpy.linspace(0.0, max_arc_length, num=max(n_samples, 2))
                sites = [_row for _row in as_curve(arc_lengths)]
        elif mode is plot_mode_e.SKL_Pixel:
            sites = list(details.sites)
        else:
            raise ValueError(
                f"{mode}: Invalid plotting mode; Valid modes: plot_mode_e.SKL_*"
            )
        sites[0], sites[1] = sites[1], TransformedY(sites[0])

        if source == target:
            edge_style = edge_styles[1]
        else:
            edge_style = edge_styles[0]
        PlotEdge(
            *sites,
            edge_style.color + edge_style.type,
            linewidth=edge_style.size,
            markersize=edge_style.size,
        )

        if direction_style.show:
            dir_sites = tuple(
                nmpy.hstack((sites[idx_][0], sites[idx_][-1]))
                for idx_ in range(space_dim)
            )
            tangents = list(zip(*InwardEndTangents(details)))
            tangents[0], tangents[1] = (
                tangents[1],
                TransformedYForVector(tangents[0]),
            )
            axes.quiver(
                *dir_sites,
                *tangents,
                color=direction_style.color,
                linewidth=direction_style.size,
            )

        if label_style.show:
            middle_idx = sites[0].size // 2
            if sites[0].size % 2 == 0:
                position = tuple(
                    nmpy.mean(_crd[(middle_idx - 1) : (middle_idx + 1)]).item()
                    for _crd in sites
                )
            else:
                position = tuple(_crd[middle_idx] for _crd in sites)
            label = PlotEdgeLabel(
                *position,
                uid,
                fontsize=label_style.size,
                color=label_style.color,
                horizontalalignment="center",
                verticalalignment="center",
            )
            label.set_bbox(_LABEL_BBOX_STYLE)
