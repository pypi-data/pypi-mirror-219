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

from typing import Sequence

import numpy as nmpy

from skl_graph.type.edge import edge_t
from skl_graph.type.node import branch_node_t, end_node_t


def Issues(
    edge: edge_t,
    source: end_node_t | branch_node_t,
    target: end_node_t | branch_node_t,
    uid: str,
    /,
) -> Sequence[str]:
    """"""
    # TODO: Check all attributes values, like with nodes, and do it first.
    output = _NodeIndependentIssues(edge)

    if not _HasValidEndSites(edge, source, target):
        output.append(f"{uid}: Invalid end sites")

    return output


def _NodeIndependentIssues(edge: edge_t, /) -> list[str]:
    """Partial validity test.

    Missing validity test: The end sites must be found in the adjacent nodes position/sites, which can only be
    tested at the graph level. See _HasValidEndSites.
    """
    output = []

    n_sites = edge.n_sites
    length = edge.lengths.length
    segment_sq_lengths = edge.lengths.segment_sq_lengths
    if length < n_sites - 1:
        output.append(
            f"{edge.uid}: {length}: Computed length cannot be smaller "
            f"than number of sites - 1={n_sites - 1}"
        )
    if nmpy.any(segment_sq_lengths == 0):
        output.append(f"{edge.uid}: Repeated sites")
    if nmpy.any(segment_sq_lengths > edge.dim):
        output.append(f"{edge.uid}: Site gaps")

    return output


def _HasValidEndSites(
    edge: edge_t,
    source: end_node_t | branch_node_t,
    target: end_node_t | branch_node_t,
    /,
) -> bool:
    """"""
    end_sites = tuple(
        tuple(edge.sites[_ddx][_sdx] for _ddx in range(edge.dim)) for _sdx in (0, -1)
    )
    n_found_end_sites = [0, 0]

    for node in (source, target):
        for e_idx in (0, 1):
            if isinstance(node, end_node_t):
                end_site_found = nmpy.array_equal(end_sites[e_idx], node.position)
            else:
                end_site = nmpy.reshape(end_sites[e_idx], (edge.dim, 1))
                end_site_found = any(
                    nmpy.all(end_site == nmpy.array(node.sites), axis=0)
                )
            if end_site_found:
                n_found_end_sites[e_idx] += 1

    if source.uid == target.uid:
        n_expected = 2
    else:
        n_expected = 1

    return n_found_end_sites == [n_expected, n_expected]
