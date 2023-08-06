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
from typing import Any

import numpy as nmpy
import skimage.measure as sims

import skl_graph.type.tpy_map as tgmp
from skl_graph.extension.number import COORDINATE_SEPARATOR

array_t = nmpy.ndarray


@dtcl.dataclass(slots=True, repr=False, eq=False)
class node_t:
    position: array_t
    uid: str = None
    properties: dict[Any, Any] = dtcl.field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        """"""
        self.uid = COORDINATE_SEPARATOR.join(map(str, self.position))

    def SetProperty(self, name: str, /, *, value: Any = None):
        """"""
        self.properties[name] = value

    @property
    def dim(self) -> int:
        """"""
        return self.position.__len__()

    def __str__(self) -> str:
        """"""
        return f"{self.__class__.__name__}.{self.uid} @ {self.position}"


@dtcl.dataclass(slots=True, repr=False, eq=False)
class end_node_t(node_t):
    diameter: float = None

    @classmethod
    def NewWithPosition(
        cls, position: array_t, /, *, width_map: array_t = None
    ) -> end_node_t:
        """"""
        output = cls(position=position)

        if width_map is not None:
            output.diameter = width_map.item(tuple(position))

        return output

    def __str__(self) -> str:
        """"""
        # super().__str__() produces:
        #     TypeError: super(type, obj): obj must be an instance or subtype of type
        # This is due to a combination of dataclass and slots=True.
        output = node_t.__str__(self)
        output += f"\n    Diameter: {self.diameter}"
        return output


@dtcl.dataclass(slots=True, repr=False, eq=False)
class branch_node_t(node_t):
    sites: tuple[array_t, ...] = None
    diameters: array_t = None

    @classmethod
    def NewWithSites(
        cls,
        sites: tuple[array_t, ...],
        /,
        *,
        width_map: array_t = None,
    ) -> branch_node_t:
        """"""
        sites_as_array = nmpy.array(sites).reshape((sites.__len__(), sites[0].size))
        centroid = nmpy.mean(sites_as_array, axis=1, keepdims=True)
        segments = sites_as_array - centroid
        medoid_idx = (segments**2).sum(axis=0).argmin()
        # nmpy.array(): fresh array instead of a view of sites_as_array
        position = nmpy.array(sites_as_array[:, medoid_idx].squeeze())

        output = cls(position=position)

        output.sites = sites
        if width_map is not None:
            output.diameters = width_map[sites]

        return output

    def __str__(self) -> str:
        """"""
        # super().__str__() produces:
        #     TypeError: super(type, obj): obj must be an instance or subtype of type
        # This is due to a combination of dataclass and slots=True.
        output = node_t.__str__(self)
        output += f"\n    Sites: {self.sites}\n    Diameters: {self.diameters}"
        return output


def EndNodes(
    tmap: array_t, /, *, width_map: array_t = None
) -> tuple[list[end_node_t], array_t]:
    """
    Note: End nodes are necessarily single-pixel nodes. Hence, they have no coordinate
    list.
    """
    # Not uint to allow for subtraction
    e_node_lmap = (tmap == 1).astype(nmpy.int64)  # Not really an lmsk here
    e_node_coords = nmpy.where(e_node_lmap)

    e_nodes: list[end_node_t] = e_node_coords[0].__len__() * [None]
    for n_idx, position in enumerate(zip(*e_node_coords)):
        end_node = end_node_t.NewWithPosition(
            nmpy.array(position, dtype=nmpy.int64), width_map=width_map
        )
        e_nodes[n_idx] = end_node
        e_node_lmap[position] = n_idx + 1  # Now that's becoming an lmsk

    return e_nodes, e_node_lmap


def BranchNodes(
    tmap: array_t, /, *, width_map: array_t = None
) -> tuple[list[branch_node_t], array_t]:
    """
    Note: Branch nodes always have a coordinate list (i.e., even if they are
    single-pixeled).
    """
    b_node_map = nmpy.logical_and(tmap > 2, tmap != tgmp.TMapBackgroundLabel(tmap))
    b_node_lmap, n_b_nodes = tgmp.LABELING_FCT_FOR_DIM[tmap.ndim](b_node_map)

    b_node_props = sims.regionprops(b_node_lmap)

    b_nodes: list[branch_node_t] = n_b_nodes * [None]
    for n_idx, props in enumerate(b_node_props):
        sites = props.image.nonzero()
        for d_idx in range(tmap.ndim):
            sites[d_idx].__iadd__(props.bbox[d_idx])
        branch_node = branch_node_t.NewWithSites(sites, width_map=width_map)
        b_nodes[n_idx] = branch_node

    return b_nodes, b_node_lmap
