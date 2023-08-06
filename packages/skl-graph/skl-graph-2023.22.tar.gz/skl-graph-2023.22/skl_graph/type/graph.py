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

"""
Base Skeleton Graph.

Simple example usage:
>>> # --- Object
>>> import skimage.data as data
>>> import skimage.util as util
>>> object_map = util.invert(data.horse())
>>> # --- SKL Map
>>> from skl_graph.type.skl_map import SKLMapFromObjectMap
>>> skl_map = SKLMapFromObjectMap(object_map)
>>> # --- SKL Graph
>>> from skl_graph.type.graph import skl_graph_t
>>> skl_graph = skl_graph_t.NewFromSKLMap(skl_map)
>>> # --- Plotting
>>> import matplotlib.pyplot as pyplot
>>> _, all_axes = pyplot.subplots(ncols=3)
>>> all_axes[0].matshow(object_map, cmap="gray")
>>> all_axes[1].matshow(skl_map, cmap="gray")
>>> from skl_graph.task.plot.graph import Plot
>>> Plot(axes=all_axes[2], should_block=False)
>>> for axes, title in zip(all_axes, ("Object", "Skeleton", "Graph")):
>>>     axes.set_title(title)
>>>     axes.set_axis_off()
>>> pyplot.tight_layout()
>>> pyplot.show()
"""

from __future__ import annotations

import inspect as nspt
from typing import Any, Sequence

import networkx as ntkx
import numpy as nmpy
import scipy.ndimage as spim
import skimage.draw as skdw

import skl_graph.type.tpy_map as tgmp
from skl_graph.extension.string import AlignedNameAndValue
from skl_graph.type.edge import EdgesFromRawEdges, RawEdges, edge_t
from skl_graph.type.node import BranchNodes, EndNodes, branch_node_t, end_node_t
from skl_graph.type.style import (
    direction_style_raw_h,
    direction_style_t,
    edge_style_raw_h,
    edge_style_t,
    edge_styles_h,
    edge_styles_raw_h,
    label_style_raw_h,
    label_style_t,
    label_styles_h,
    label_styles_raw_h,
    node_either_raw_h,
    node_style_t,
    node_styles_h,
)

array_t = nmpy.ndarray


class skl_graph_t(ntkx.MultiGraph):
    """
    s_node: Singleton node
    e_node: End node
    b_node: Branch node
    """

    __slots__ = (
        "domain_shape",
        "n_components",
        "n_s_nodes",
        "n_e_nodes",
        "n_b_nodes",
        "has_widths",
        "node_styles",
        "edge_styles",
        "direction_style",
        "label_styles",
    )
    domain_shape: tuple[int, ...]
    n_components: int
    n_s_nodes: int
    n_e_nodes: int
    n_b_nodes: int
    has_widths: bool
    node_styles: node_styles_h  # One style per degree + one default style
    edge_styles: edge_styles_h  # One style for "regular" edges, one for self-loops
    direction_style: direction_style_t
    label_styles: label_styles_h  # For nodes and edges, in that order

    def __init__(self) -> None:
        """"""
        super().__init__()
        for slot in skl_graph_t.__slots__:
            setattr(self, slot, None)

    @classmethod
    def NewFromSKLMap(
        cls, skl_map: array_t, /, *, width_map: array_t = None
    ) -> skl_graph_t:
        """

        Parameters
        ----------
        skl_map : numpy.ndarray
        width_map : numpy.ndarray, optional

        Returns
        -------
        skl_graph_t
            Graph of the skeleton as an extended networkx.MultiGraph instance
        """
        output = cls()

        output.domain_shape = skl_map.shape
        output.has_widths = width_map is not None
        output.n_s_nodes = 0
        output.n_e_nodes = 0
        output.n_b_nodes = 0

        tmap, background_label = tgmp.TopologyMapOfMap(skl_map, return_bg_label=True)
        cc_map, n_components = tgmp.LABELING_FCT_FOR_DIM[skl_map.ndim](skl_map)

        output.n_components = n_components

        # Process skl_map/tmap per connected component (*)
        for cmp_label in range(1, n_components + 1):
            if n_components > 1:
                single_skl_map = cc_map == cmp_label
                single_tmap = nmpy.full_like(tmap, background_label)
                single_tmap[single_skl_map] = tmap[single_skl_map]
            else:
                single_skl_map = skl_map > 0
                single_tmap = tmap

            if output._DealsWithSpecialCases(
                single_tmap, background_label, width_map=width_map
            ):
                pass
            else:
                e_nodes, e_node_lmap = EndNodes(single_tmap, width_map=width_map)
                b_nodes, b_node_lmap = BranchNodes(single_tmap, width_map=width_map)
                raw_edges, edge_lmap = RawEdges(single_skl_map, b_node_lmap)
                edges, node_uids_per_edge = EdgesFromRawEdges(
                    raw_edges,
                    e_nodes,
                    b_nodes,
                    edge_lmap,
                    e_node_lmap,
                    b_node_lmap,
                    width_map=width_map,
                )

                output.add_nodes_from((_nde.uid, {"details": _nde}) for _nde in e_nodes)
                output.add_nodes_from((_nde.uid, {"details": _nde}) for _nde in b_nodes)
                for edge, adjacent_node_uids in zip(edges, node_uids_per_edge):
                    output.AddEdge(edge, adjacent_node_uids)

                output.n_e_nodes += e_nodes.__len__()
                output.n_b_nodes += b_nodes.__len__()

        output.node_styles = node_style_t.Default()
        output.edge_styles = edge_style_t.Default()
        output.direction_style = direction_style_t.Default()
        output.label_styles = label_style_t.Default()

        return output

    def _DealsWithSpecialCases(
        self, tmap: array_t, background_label: int, /, *, width_map: array_t = None
    ) -> bool:
        """Creates and adds nodes and edges of cases such as a singleton node, self loops...

        Parameters
        ----------
        tmap : numpy.ndarray
            Topological map of the skeleton; Must contain a unique connected component.
        background_label
        width_map

        Returns
        -------

        """
        singleton = nmpy.where(tmap == 0)
        if singleton[0].size > 0:
            # Can only be 1 since tmap is processed per connected components (*)
            singleton = nmpy.array(singleton, dtype=nmpy.int64).squeeze()
            _ = self.AddEndNode(singleton, width_map=width_map, is_singleton=True)

            return True
        #
        elif (tmap[tmap != background_label] == 2).all():
            # The tmap represents a self loop
            loop_slc = nmpy.nonzero(tmap == 2)

            # Takes the first pixel to serve as a node, and the rest for the self-loop edge
            #
            # 0:1 makes sites elements array_t's (instead of Numpy numbers), which is necessary for
            # branch_node_t.NewWithSites.
            sites = tuple(per_dim[0:1] for per_dim in loop_slc)
            node_uid = self.AddBranchNode(sites, width_map=width_map)

            n_unique_sites = loop_slc[0].__len__()
            sites = tuple(
                per_dim[list(range(n_unique_sites)) + [0]] for per_dim in loop_slc
            )
            adjacent_node_uids = (node_uid, node_uid)
            edge = edge_t.NewWithDetails(
                sites,
                False,
                adjacent_node_uids,
                width_map=width_map,
            )
            self.AddEdge(edge, adjacent_node_uids)

            return True

        return False

    def AddEndNode(
        self,
        position: array_t,
        /,
        *,
        width_map: array_t = None,
        is_singleton: bool = False,
    ) -> Any:
        """"""
        node = end_node_t.NewWithPosition(position, width_map=width_map)
        self.add_node(node.uid, details=node)

        if is_singleton:
            self.n_s_nodes += 1

        return node.uid

    def AddBranchNode(
        self,
        sites: tuple[array_t, ...],
        /,
        *,
        width_map: array_t = None,
    ) -> Any:
        """"""
        node = branch_node_t.NewWithSites(sites, width_map=width_map)
        self.add_node(node.uid, details=node)

        self.n_b_nodes += 1

        return node.uid

    def AddEdge(self, edge: edge_t, adjacent_node_uids: Sequence[str], /) -> None:
        """"""
        edge_uid = edge.uid
        version_number = 0
        uid_w_vn = edge_uid
        while self.has_edge(*adjacent_node_uids, key=uid_w_vn):
            version_number += 1
            uid_w_vn = edge_uid + "+" + version_number.__str__()

        # The key is added to distinguish between multiple "parallel" edges. As a consequence, an edge is accessed as
        # follows: self.edges[adjacent_node_uids[0], adjacent_node_uids[1], uid_w_vn]
        self.add_edge(*adjacent_node_uids, key=uid_w_vn, details=edge)

    @property
    def dim(self) -> int:
        """"""
        return self.domain_shape.__len__()

    @property
    def n_nodes(self) -> int:
        """"""
        return self.number_of_nodes()

    @property
    def n_edges(self) -> int:
        """"""
        return self.number_of_edges()

    @property
    def n_self_loops(self) -> int:
        """"""
        return ntkx.number_of_selfloops(self)

    @property
    def degree_statistics(self) -> tuple[int, int, float, float, float, array_t]:
        """"""
        degrees = tuple(degree for _, degree in self.degree)
        return (
            min(degrees),
            max(degrees),
            nmpy.median(degrees).item(),
            nmpy.mean(degrees).item(),
            nmpy.std(degrees).item(),
            nmpy.bincount(degrees),
        )

    @property
    def least_and_most_connected_nodes(
        self,
    ) -> tuple[tuple[str, ...], int, tuple[str, ...], int]:
        """"""
        min_degree, max_degree, *_ = self.degree_statistics
        least = (_nde for _nde, _dgr in self.degree if _dgr == min_degree)
        most = (_nde for _nde, _dgr in self.degree if _dgr == max_degree)

        return tuple(least), min_degree, tuple(most), max_degree

    @property
    def length(self) -> float:
        """"""
        return sum(_lgt for *_, _lgt in self.lengths)

    @property
    def lengths(self) -> tuple[tuple[str, str, str, float], ...]:
        """"""
        # TODO: check that the newly retrieved uid does not break calls.
        return tuple(
            (_src, _tgt, _uid, _dtl.lengths.length)
            for _src, _tgt, _uid, _dtl in self.edges.data("details", keys=True)
        )

    @property
    def mean_based_area(self) -> float:
        """
        See self.mean_based_areas
        """
        return sum(_are for *_, _are in self.mean_based_areas)

    @property
    def mean_based_areas(self) -> tuple[tuple[str, str, str, float], ...]:
        """
        mean=using mean edge widths
        """
        # TODO: check that the newly retrieved uid does not break code.
        if self.has_widths:
            return tuple(
                (_src, _tgt, _uid, _dtl.areas.mean_based_area)
                for _src, _tgt, _uid, _dtl in self.edges.data("details", keys=True)
            )

        return self.n_edges * (("", "", "", 0.0),)

    @property
    def segment_based_area(self) -> float:
        """
        See self.segment_based_areas
        """
        return sum(_are for *_, _are in self.segment_based_areas)

    @property
    def segment_based_areas(self) -> tuple[tuple[str, str, str, float], ...]:
        """
        segment=using edge segments
        """
        # TODO: check that the newly retrieved uid does not break code.
        if self.has_widths:
            return tuple(
                (_src, _tgt, _uid, _dtl.areas.segment_based_area)
                for _src, _tgt, _uid, _dtl in self.edges.data("details", keys=True)
            )

        return self.n_edges * (("", "", "", 0.0),)

    @property
    def bbox(self) -> tuple[int, ...]:
        """"""
        bbox_min = nmpy.full(self.dim, max(self.domain_shape), dtype=nmpy.int64)
        bbox_max = nmpy.zeros(self.dim, dtype=nmpy.int64)
        for *_, edge in self.edges.data("details"):
            sites = nmpy.array(edge.sites, dtype=nmpy.int64)
            bbox_min = nmpy.fmin(bbox_min, nmpy.amin(sites, axis=1))
            bbox_max = nmpy.fmax(bbox_max, nmpy.amax(sites, axis=1))

        output = []
        for d_idx in range(self.dim):
            output.extend((bbox_min[d_idx], bbox_max[d_idx]))

        return tuple(output)

    def AsNetworkX(self) -> ntkx.MultiGraph:
        """"""
        return ntkx.MultiGraph(incoming_graph_data=self)
        # TODO: Why storing uid in edge while it is already available as source, target, uid?
        # output = ntkx.MultiGraph(incoming_graph_data=self)
        #
        # for source, target, details in self.edges.data("details"):
        #     uid = details.uid
        #     output.edges[source, target, uid]["uid"] = uid
        #
        # return output

    def RebuiltSkeletonMap(self, /, *, with_width: bool = False) -> array_t:
        """"""
        if (not self.has_widths) and with_width:
            with_width = False
        if with_width:
            dtype = nmpy.float64
        else:
            # Not uint to allow for subtraction
            dtype = nmpy.int8

        output = nmpy.zeros(self.domain_shape, dtype=dtype)

        for *_, details in self.edges.data("details"):
            if with_width:
                output[details.sites] = details.widths
            else:
                output[details.sites] = 2

        for _, details in self.nodes.data("details"):
            if isinstance(details, branch_node_t):
                if with_width:
                    output[details.sites] = details.diameters
                else:
                    output[details.sites] = 3
            else:
                if with_width:
                    output[tuple(details.position)] = details.diameter
                else:
                    output[tuple(details.position)] = 1

        return output

    def RebuiltObjectMap(self) -> array_t:
        """"""
        if not self.has_widths:
            raise ValueError("Requires an SKL graph with widths")

        # Not uint to allow for subtraction
        output = nmpy.zeros(self.domain_shape, dtype=nmpy.int8)

        if self.dim == 2:
            NewBall = skdw.disk
        else:
            NewBall = _Ball3D

        for _, details in self.nodes.data("details"):
            if isinstance(details, branch_node_t):
                for *sites, radius in zip(
                    *details.sites,
                    nmpy.around(0.5 * (details.diameters - 1.0)).astype(nmpy.int64),
                ):
                    output[NewBall(sites, radius, shape=output.shape)] = 1
            else:
                output[
                    NewBall(
                        details.position,
                        nmpy.around(0.5 * (details.diameter - 1.0))
                        .astype(nmpy.int64)
                        .item(),
                        shape=output.shape,
                    )
                ] = 1

        for *_, details in self.edges.data("details"):
            for *sites, radius in zip(
                *details.sites,
                nmpy.around(0.5 * (details.widths - 1.0)).astype(nmpy.int64),
            ):
                output[NewBall(sites, radius, shape=output.shape)] = 1

        return output

    def SetPlotStyles(
        self,
        /,
        *,
        node: node_either_raw_h = None,
        #
        edge: edge_style_raw_h = None,
        regular_edge: edge_style_raw_h = None,
        self_loop: edge_style_raw_h = None,
        edges: edge_styles_raw_h = None,
        #
        label: label_style_raw_h = None,
        label_node: label_style_raw_h = None,
        label_edge: label_style_raw_h = None,
        labels: label_styles_raw_h = None,
        #
        direction: direction_style_raw_h = None,
    ) -> None:
        """
        edge: common style for both regulars and self-loops
        edges: styles for regulars and self-loops, in that order
        label: common style for both nodes and edges
        labels: styles for nodes and edges, in that order
        """
        if node is not None:
            styles = node_style_t.NewFromUnstructured(node)
            if isinstance(node, dict):  # node_styles_raw_h
                self.node_styles.update(styles)
            else:
                self.node_styles = styles
            if None not in self.node_styles:
                # Should never happen, but just in case...
                raise ValueError(
                    f"{self.node_styles}: Node styles without default style. "
                    f'Expected: style dictionary with a "None" entry.'
                )

        styles = edge_style_t.AllFromUnstructured(
            self.edge_styles,
            edge=edge,
            regular_edge=regular_edge,
            self_loop=self_loop,
            edges=edges,
        )
        if styles is not None:
            self.edge_styles = styles

        styles = label_style_t.AllFromUnstructured(
            self.label_styles,
            label=label,
            node=label_node,
            edge=label_edge,
            labels=labels,
        )
        if styles is not None:
            self.label_styles = styles

        if direction is not None:
            self.direction_style = direction_style_t.NewFromUnstructured(direction)

    def Properties(self, /, *, prefix: str = "") -> str:
        """"""
        output = []

        max_name_length = 0
        # The loop below seems unnecessarily complicated. But the simpler call
        # "nspt.getmembers(self, lambda _elm: isinstance(_elm, property))" does not work since _elm is the actual value,
        # so...
        for name, value in nspt.getmembers(self):
            # Somehow, a name returned by getmembers might not be an attribute of the class !
            attribute = getattr(self.__class__, name, None)
            if attribute is None:
                continue

            if isinstance(attribute, property) and not isinstance(value, Sequence):
                if (current_length := name.__len__()) > max_name_length:
                    max_name_length = current_length
                output.append(f"{name}: {value}")
        output = map(
            lambda _elm: AlignedNameAndValue(_elm, max_name_length + 1, prefix), output
        )

        return "\n".join(output)

    def __str__(self) -> str:
        """"""
        output = (
            f"{self.__class__.__name__}:\n"
            f"    Domain shape: {self.domain_shape}\n"
            f"    Has widths:   {self.has_widths}\n\n"
            f"    Components:   {self.n_components}\n"
            f"    Nodes:        {self.n_nodes}"
            f" = S_{self.n_s_nodes} + E_{self.n_e_nodes} + B_{self.n_b_nodes}\n"
            f"    Edges:        {self.n_edges}, among which {self.n_self_loops} self loop(s)"
        )

        return output


def _Ball3D(
    center: Sequence[int], radius: int, /, *, shape: tuple[int, int, int] = None
) -> array_t:
    """
    Signature follows the one of skimage.draw.disk
    """
    output = nmpy.zeros(shape, dtype=nmpy.bool_)
    # skdw.ellipsoid leaves a one pixel margin around the ellipse, hence [1:-1, 1:-1, 1:-1]
    ellipse = skdw.ellipsoid(radius, radius, radius)[1:-1, 1:-1, 1:-1]
    sp_slices = tuple(
        slice(0, min(output.shape[idx_], ellipse.shape[idx_])) for idx_ in (0, 1, 2)
    )
    output[sp_slices] = ellipse[sp_slices]

    row, col, dep = center
    output = spim.shift(
        output, (row - radius, col - radius, dep - radius), order=0, prefilter=False
    )

    return output
