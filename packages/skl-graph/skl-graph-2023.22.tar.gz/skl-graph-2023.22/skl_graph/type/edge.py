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

from __future__ import annotations

import dataclasses as dtcl
from typing import Any, Sequence

import numpy as nmpy
import scipy.interpolate as spnt
import skimage.measure as sims

import skl_graph.type.tpy_map as tgmp
from skl_graph.extension.number import COORDINATE_SEPARATOR, EncodedNumber
from skl_graph.type.feature import areas_t, lengths_t
from skl_graph.type.node import branch_node_t, end_node_t, node_t

array_t = nmpy.ndarray


_MAX_SQ_INTERPOLATION_ERROR = 0.8**2


@dtcl.dataclass(slots=True, repr=False, eq=False)
class raw_edge_t:
    """
    /!\ "sites" is organized by dimension, not by site. This is why "dim" is defined as self.sites.__len__() instead of
    self.sites[0].size.
    """

    sites: tuple[array_t, ...]

    @property
    def dim(self) -> int:
        """"""
        return self.sites.__len__()

    @property
    def n_sites(self) -> int:
        """
        Cannot be less than 2 since even an edge between an end node and a touching branch node will contain the end
        node pixel and one branch node pixel.
        """
        return self.sites[0].size


@dtcl.dataclass(slots=True, repr=False, eq=False)
class edge_t(raw_edge_t):
    uid: str = None
    lengths: lengths_t = None
    widths: array_t = None
    areas: areas_t = None
    properties: dict[Any, Any] = dtcl.field(init=False, default_factory=dict)
    _cache: dict[str, Any] = dtcl.field(default_factory=dict)

    @classmethod
    def NewWithDetails(
        cls,
        sites: tuple[array_t, ...],
        sites_are_ordered: bool,
        adjacent_node_uids: Sequence[str],
        /,
        *,
        width_map: array_t = None,
    ) -> edge_t:
        """"""
        if sites_are_ordered:
            ordered_sites = sites
        else:
            ordered_sites = _ReOrderedSites(sites)

        output = cls(ordered_sites)

        output.uid = _UID(adjacent_node_uids)
        output.lengths = lengths_t.NewFromSites(ordered_sites)
        if width_map is not None:
            output.widths = width_map[ordered_sites]
            output.areas = areas_t.NewFromLengthsAndWidths(
                output.lengths, output.widths
            )

        return output

    def SetProperty(self, name: str, /, *, value: Any = None):
        """"""
        self.properties[name] = value

    @property
    def arc_lengths(self) -> array_t:
        """
        Arc length coordinates of each pixel/voxel composing the edge.
        """
        output = nmpy.cumsum((0.0,) + tuple(self.lengths.segment_lengths))
        output[-1] = self.lengths.length  # To correct round-off errors.
        assert output[-1] > output[-2]  # To check above correction was not invalid.

        return output

    def AsCurve(self) -> spnt.PchipInterpolator | None:
        """"""
        cache_entry = self.AsCurve.__name__

        if cache_entry not in self._cache:
            if self.n_sites > 3:
                self._cache[cache_entry] = _PchipInterpolator(
                    self.arc_lengths, nmpy.array(self.sites)
                )
            else:
                self._cache[cache_entry] = None

        return self._cache[cache_entry]

    def __str__(self) -> str:
        """
        Does not call raw_edge_t.__str__ since raw edges do not have UID
        """
        origin = tuple(self.sites[_idx][0] for _idx in range(self.dim))
        raw_length = round(self.lengths.length, 2)
        if self.areas is None:
            segment_based_area = raw_length
        else:
            segment_based_area = round(self.areas.segment_based_area, 2)

        main = (
            f"{self.__class__.__name__}.{self.uid}:\n"
            f"    Sites[{self.dim}-D]: {self.n_sites}\n"
            f"    Origin:              {origin}\n"
            f"    Lengths:             Raw={raw_length}, SB-Area={segment_based_area}"
        )

        if (self._cache is None) or (self._cache.__len__() == 0):
            cached_values = "None yet"
        else:
            cached_values = ", ".join(self._cache.keys())

        return main + f"\n    Cached values: {cached_values}"


@dtcl.dataclass(slots=True, repr=False, eq=False)
class _transient_t(raw_edge_t):
    def __post_init__(self) -> None:
        """"""
        self.sites = _ReOrderedSites(self.sites)

    def AppendBranchNode(
        self,
        b_coords: array_t,
        node: node_t,
        adjacent_node_uids: list[str],
        /,
        *,
        force_after: bool = False,
    ) -> None:
        """"""
        adjacent_node_uids.append(node.uid)

        space_dim = self.dim
        first_site = tuple(self.sites[idx_][0] for idx_ in range(space_dim))
        sq_distance = (nmpy.subtract(first_site, b_coords) ** 2).sum()

        if self.n_sites > 1:
            # 0 <: so that if the edge is a self-loop ending at the same site, it does not put twice the site in a row
            if 0 < sq_distance <= space_dim:
                self.sites = tuple(
                    nmpy.hstack((b_coords[idx_], self.sites[idx_]))
                    for idx_ in range(space_dim)
                )
            else:
                self.sites = tuple(
                    nmpy.hstack((self.sites[idx_], b_coords[idx_]))
                    for idx_ in range(space_dim)
                )
        elif force_after:
            self.sites = tuple(
                nmpy.hstack((self.sites[idx_], b_coords[idx_]))
                for idx_ in range(space_dim)
            )
        else:
            self.sites = tuple(
                nmpy.hstack((b_coords[idx_], self.sites[idx_]))
                for idx_ in range(space_dim)
            )


def RawEdges(
    skl_map: array_t, b_node_lmap: array_t, /
) -> tuple[Sequence[raw_edge_t], array_t]:
    """"""
    edge_map = skl_map.astype(nmpy.int8)
    edge_map[b_node_lmap > 0] = 0
    edge_lmap, n_edges = tgmp.LABELING_FCT_FOR_DIM[skl_map.ndim](edge_map)

    edge_props = sims.regionprops(edge_lmap)

    edges: list[raw_edge_t] = n_edges * [None]
    for props in edge_props:
        sites = props.image.nonzero()
        for d_idx in range(skl_map.ndim):
            sites[d_idx].__iadd__(props.bbox[d_idx])
        edges[props.label - 1] = raw_edge_t(sites)

    return edges, edge_lmap


def EdgesFromRawEdges(
    raw_edges: Sequence[raw_edge_t],
    e_nodes: Sequence[end_node_t],
    b_nodes: Sequence[branch_node_t],
    edge_lmap: array_t,
    e_node_lmap: array_t,
    b_node_lmap: array_t,
    /,
    *,
    width_map: array_t = None,
) -> tuple[tuple[edge_t], list[list[str]]]:
    """"""
    transient_edges = tuple(map(lambda _raw: _transient_t(_raw.sites), raw_edges))
    edge_tmap = tgmp.TopologyMapOfMap(edge_lmap > 0)

    # ep=edge end point; Keep < 2 since ==0 (length-1 edges) and ==1 (other edges) are needed
    # Do not use list multiplication since the same list then used for all the elements
    node_uids_per_edge: list[list[str]] = [[] for _ in transient_edges]
    for ep_coords in zip(*(edge_tmap < 2).nonzero()):
        edge_idx = edge_lmap[ep_coords] - 1
        transient = transient_edges[edge_idx]
        e_node_label = e_node_lmap[ep_coords]

        if e_node_label > 0:
            # End node-to-X edge (i.e., edge end point is also an end node)
            node_uids_per_edge[edge_idx].append(e_nodes[e_node_label - 1].uid)
            if transient.n_sites == 1:
                # End node-to-branch node edge (and there is a unique non-zero value in b_neighborhood)
                nh_slices_starts, b_neighborhood = _LMapNeighborhood(
                    b_node_lmap, ep_coords
                )
                b_node_label = nmpy.amax(b_neighborhood)
                b_coords = nmpy.transpose((b_neighborhood == b_node_label).nonzero())[0]
                transient.AppendBranchNode(
                    nmpy.add(nh_slices_starts, b_coords),
                    b_nodes[b_node_label - 1],
                    node_uids_per_edge[edge_idx],
                )
        else:
            nh_slices_starts, b_neighborhood = _LMapNeighborhood(b_node_lmap, ep_coords)
            force_after = False
            # Looping only for length-1, b-to-b edges
            for b_coords in zip(*b_neighborhood.nonzero()):
                b_node_label = b_neighborhood[b_coords]
                transient.AppendBranchNode(
                    nmpy.add(nh_slices_starts, b_coords),
                    b_nodes[b_node_label - 1],
                    node_uids_per_edge[edge_idx],
                    force_after=force_after,
                )
                force_after = not force_after

    edges = []
    for transient, adjacent_node_uids in zip(transient_edges, node_uids_per_edge):
        # Fix sites order for self-loops connected to branch nodes
        if adjacent_node_uids[0] == adjacent_node_uids[1]:
            node = None
            for current in b_nodes:
                if current.uid == adjacent_node_uids[0]:
                    node = current
                    break
            if node is not None:
                node_sites = nmpy.array(node.sites)
                edge_sites = nmpy.array(transient.sites)
                while not all(
                    any(
                        nmpy.all(
                            (node_sites - edge_sites[:, _sdx][:, None]) == 0, axis=0
                        )
                    )
                    for _sdx in (0, -1)
                ):
                    edge_sites = nmpy.roll(edge_sites, -1, axis=1)

                transient.sites = tuple(
                    edge_sites[_cdx, :] for _cdx in range(transient.dim)
                )

        edge = edge_t.NewWithDetails(
            transient.sites, True, adjacent_node_uids, width_map=width_map
        )
        edges.append(edge)

    return tuple(edges), node_uids_per_edge


def _ReOrderedSites(sites: tuple[array_t, ...], /) -> tuple[array_t, ...]:
    """
    If the number of sites is 1 or 2, the input argument is returned (i.e., no copy is made).
    """
    n_sites = sites[0].size
    if n_sites < 3:
        return sites

    dim = sites.__len__()

    self_loop = all(sites[idx][0] == sites[idx][-1] for idx in range(dim))
    if self_loop:
        sites = tuple(sites[idx][:-1] for idx in range(dim))
        n_sites -= 1
        self_origin = nmpy.fromiter(
            (sites[idx][0] for idx in range(dim)), dtype=sites[0].dtype
        )
        self_origin = nmpy.reshape(self_origin, (1, dim))
    else:
        self_origin = None

    sites_as_array = nmpy.transpose(nmpy.array(sites))
    reordered_coords = [nmpy.array([sites[idx][0] for idx in range(sites.__len__())])]
    unvisited_slc = nmpy.ones(n_sites, dtype=nmpy.bool_)
    unvisited_slc[0] = False
    unvisited_sites = None
    end_point = None
    pre_done = False
    post_done = False

    while unvisited_slc.any():
        if post_done:
            neighbor_idc = ()
        else:
            end_point = reordered_coords[-1]
            neighbor_idc, unvisited_sites = _NeighborIndices(
                dim, sites_as_array, unvisited_slc, end_point
            )

        if (neighbor_idc.__len__() == 1) or post_done:
            also_grow_first = (reordered_coords.__len__() > 1) and not pre_done
            if not post_done:
                c_idx = neighbor_idc[0]
                reordered_coords.append(unvisited_sites[c_idx, :])
                unvisited_slc[nmpy.where(unvisited_slc)[0][c_idx]] = False
            if also_grow_first:
                end_point = reordered_coords[0]
                neighbor_idc, unvisited_sites = _NeighborIndices(
                    dim, sites_as_array, unvisited_slc, end_point
                )
                if neighbor_idc.__len__() == 1:
                    c_idx = neighbor_idc[0]
                    reordered_coords = [unvisited_sites[c_idx, :]] + reordered_coords
                    unvisited_slc[nmpy.where(unvisited_slc)[0][c_idx]] = False
                elif neighbor_idc.__len__() == 0:
                    pre_done = True  # End point has been reached
                else:
                    raise RuntimeError(
                        f"{neighbor_idc.__len__()} neighbors when only 1 is expected\n"
                        f"{sites}\n{reordered_coords}\n{unvisited_slc}\n{end_point}"
                    )
        elif neighbor_idc.__len__() == 2:
            if reordered_coords.__len__() == 1:
                idx1, idx2 = neighbor_idc
                reordered_coords = [unvisited_sites[idx1, :]] + reordered_coords
                reordered_coords.append(unvisited_sites[idx2, :])
                true_map = nmpy.where(unvisited_slc)[0]
                unvisited_slc[true_map[idx1]] = False
                unvisited_slc[true_map[idx2]] = False
            else:
                raise RuntimeError(
                    f"2 neighbors when only 1 is expected\n"
                    f"{sites}\n{reordered_coords}\n{unvisited_slc}\n{end_point}"
                )
        elif neighbor_idc.__len__() == 0:
            post_done = True  # End point has been reached
        else:
            raise RuntimeError(
                f"{neighbor_idc.__len__()} neighbors when only 1 or 2 are expected\n"
                f"{sites}\n{reordered_coords}\n{unvisited_slc}\n{end_point}"
            )

    reordered_coords = nmpy.array(reordered_coords)
    if self_loop:
        reordered_coords = _RolledSitesWithFixedOrigin(reordered_coords, self_origin)
    reordered_coords = tuple(reordered_coords[:, _idx] for _idx in range(dim))

    return reordered_coords


def _NeighborIndices(
    dim: int, sites: array_t, unvisited_slc: array_t, end_point: array_t
) -> tuple[array_t, array_t]:
    """"""
    unvisited_sites = sites[unvisited_slc, :]

    distances = nmpy.fabs(unvisited_sites - nmpy.reshape(end_point, (1, dim)))
    neighbor_idc = nmpy.nonzero(nmpy.all(distances <= 1, axis=1))[0]

    return neighbor_idc, unvisited_sites


def _RolledSitesWithFixedOrigin(sites: array_t, origin: array_t, /) -> array_t:
    """"""
    self_origin_idx = nmpy.argwhere(nmpy.all(sites == origin, axis=1)).item()
    if self_origin_idx > 0:
        sites = nmpy.roll(sites, -self_origin_idx, axis=0)

    return nmpy.vstack((sites, origin))


def _LMapNeighborhood(lmap: array_t, site: tuple[int, ...]) -> tuple[array_t, array_t]:
    """"""
    slices_starts = tuple(max(site[idx_] - 1, 0) for idx_ in range(site.__len__()))
    slices = tuple(
        slice(slices_starts[idx_], min(site[idx_] + 2, lmap.shape[idx_]))
        for idx_ in range(site.__len__())
    )
    neighborhood = lmap[slices]

    return nmpy.array(slices_starts, dtype=nmpy.int64), neighborhood


def _PchipInterpolator(
    arc_lengths: array_t, sites: array_t, /
) -> spnt.PchipInterpolator:
    """"""
    for n_samples in range(2, arc_lengths.size + 1):
        arc_length_samples = nmpy.linspace(0, arc_lengths.size - 1, num=n_samples)
        indices = nmpy.unique(nmpy.around(arc_length_samples)).astype(nmpy.uint64)
        output = spnt.PchipInterpolator(
            arc_lengths[indices], sites[:, indices], axis=1, extrapolate=False
        )

        error = max(nmpy.sum((output(arc_lengths) - sites) ** 2, axis=0))
        if error <= _MAX_SQ_INTERPOLATION_ERROR:
            return output

    raise RuntimeError("Should never happen. Please contact developer.")


def _UID(adjacent_node_uids: Sequence[str], /) -> str:
    """"""
    if adjacent_node_uids.__len__() != 2:
        raise RuntimeError(
            f"{adjacent_node_uids.__len__()}: Incorrect number of adjacent node uids"
        )

    node_uid_0, node_uid_1 = adjacent_node_uids
    if node_uid_0 > node_uid_1:
        node_uid_0, node_uid_1 = node_uid_1, node_uid_0

    uid_components = [
        EncodedNumber(coord) for coord in node_uid_0.split(COORDINATE_SEPARATOR)
    ]
    uid_components.append(COORDINATE_SEPARATOR)
    uid_components.extend(
        EncodedNumber(coord) for coord in node_uid_1.split(COORDINATE_SEPARATOR)
    )

    return "".join(uid_components)
