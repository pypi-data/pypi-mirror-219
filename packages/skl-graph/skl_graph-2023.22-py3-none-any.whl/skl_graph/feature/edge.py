# Copyright CNRS/Inria/UCA
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

import numpy as nmpy

from skl_graph.type.edge import edge_t

array_t = nmpy.ndarray


def InwardEndTangents(edge: edge_t, /) -> tuple[array_t, array_t]:
    """"""
    cache_entry = InwardEndTangents.__name__

    if cache_entry not in edge._cache:
        first_inner, last_inner = _InwardEndSegments(edge)
        flips = [1.0, 1.0]

        as_curve = edge.AsCurve()
        if as_curve is None:
            if edge.n_sites > 1:
                first_tangent = nmpy.array(first_inner, dtype=nmpy.float64)
                last_tangent = nmpy.array(last_inner, dtype=nmpy.float64)
            else:
                raise RuntimeError("Should never happen. Please contact developer.")
        else:
            max_arc_length = as_curve.x.item(-1)
            derivatives = as_curve((0, max_arc_length), 1)
            first_tangent = nmpy.array(derivatives[:, 0], dtype=nmpy.float64)
            last_tangent = nmpy.array(derivatives[:, 1], dtype=nmpy.float64)
            for p_idx, product in enumerate(
                (
                    nmpy.dot(first_tangent, first_inner),
                    nmpy.dot(last_tangent, last_inner),
                )
            ):
                if product < 0.0:
                    flips[p_idx] = -1.0
        first_tangent /= flips[0] * nmpy.linalg.norm(first_tangent)
        last_tangent /= flips[1] * nmpy.linalg.norm(last_tangent)
        edge._cache[cache_entry] = (first_tangent, last_tangent)

    return edge._cache[cache_entry]


def Tangents(edge: edge_t, /) -> tuple[array_t, array_t, array_t]:
    """"""
    cache_entry = Tangents.__name__

    if cache_entry not in edge._cache:
        as_curve = edge.AsCurve()
        if as_curve is None:
            if edge.n_sites > 1:
                sites = nmpy.array(edge.sites)
                arc_lengths = edge.arc_lengths
                derivatives = nmpy.diff(sites, axis=1).astype(nmpy.float64)
                norms = nmpy.linalg.norm(derivatives, axis=0, keepdims=True)
                derivatives /= norms
                last = derivatives[:, -1][:, None]
                tangents = nmpy.hstack((derivatives, last))
            else:
                raise RuntimeError("Should never happen. Please contact developer.")
        else:
            arc_lengths = as_curve.x
            sites, derivatives = (as_curve(arc_lengths, _rdr) for _rdr in (0, 1))
            norms = nmpy.linalg.norm(derivatives, axis=0, keepdims=True)
            tangents = derivatives / norms
        edge._cache[cache_entry] = (sites, arc_lengths, tangents)

    return edge._cache[cache_entry]


def TangentDirectionChanges(edge: edge_t, /) -> array_t:
    """
    2-D: determinant of consecutive tangents, normalized by arc length differences.
    3-D: "signed" norm of the cross product of consecutive tangents, normalized by arc length differences.
    """
    cache_entry = TangentDirectionChanges.__name__

    if cache_entry not in edge._cache:
        if edge.dim == 2:
            Determinant = lambda _vct, _ref: (nmpy.linalg.det(_vct), _ref)
        else:
            Determinant = _SignedCrossProductNorm

        _, arc_lengths, tangents = Tangents(edge)
        determinants = nmpy.empty((tangents.shape[1] - 1), dtype=nmpy.float64)
        reference = None
        for c_idx in range(tangents.shape[1] - 1):
            determinants[c_idx], reference = Determinant(
                tangents[:, c_idx : (c_idx + 2)], reference
            )
        determinants /= arc_lengths[1:]
        edge._cache[cache_entry] = determinants

    return edge._cache[cache_entry]


def Tortuosity(edge: edge_t, /) -> float:
    """
    https://en.wikipedia.org/wiki/Tortuosity
    """
    chord_length = nmpy.linalg.norm(edge.sites[0] - edge.sites[-1])
    return edge.lengths.length / chord_length


def _InwardEndSegments(edge: edge_t, /) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """"""
    dim_range = tuple(range(edge.dim))
    first_inner = tuple(edge.sites[_idx][1] - edge.sites[_idx][0] for _idx in dim_range)
    last_inner = tuple(
        edge.sites[_idx][-2] - edge.sites[_idx][-1] for _idx in dim_range
    )

    return first_inner, last_inner


def _SignedCrossProductNorm(
    vectors: array_t, reference: array_t | None, /
) -> tuple[float, array_t]:
    """"""
    product = nmpy.cross(vectors[:, 0], vectors[:, 1])
    if reference is None:
        reference = product
        sign = 1.0
    else:
        sign = nmpy.dot(product, reference)

    return (sign * nmpy.linalg.norm(product)).item(), reference
