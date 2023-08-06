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

from typing import Optional

import numpy as nmpy

import skl_graph.type.tpy_map as tymp

array_t = nmpy.ndarray


def CheckSkeletonMap(
    skl_map: array_t,
    /,
    *,
    mode: Optional[str] = "single",
    behavior: Optional[str] = "exception",
) -> list[str] | None:
    """Raises an exception or returns a list of invalid properties if the passed map is not a valid skeleton map.

    The map dtype is not strictly checked: only floating point types raise an exception (but int64, for example, does
    not although the chosen definition for skeleton map only mentions boolean and 8-bit integer types). The other
    aspects of a valid skeleton map are described in the module documentation.

    Parameters
    ----------
    skl_map : numpy.ndarray
    mode : str, optional
        Can be "single" (the default) to check that `skl_map` is a valid skeleton map with a unique connected component,
        or "multi" if multiple connected components are allowed. It can also be None to skip validation.
    behavior : str, optional
        Can be "exception" (the default) to trigger an exception raising if the map is invalid, or "report" to just
        return None if the map is valid or a list of strings describing the invalid properties.

    Returns
    -------
    list[str], optional

    """
    # TODO: Fully check skl_map validity, like with node position, and do it first.
    if mode is None:
        return None

    if mode == "single":
        output = _SingleSkeletonMapIssues(skl_map)
    elif mode == "multi":
        output = _MultiSkeletonMapIssues(skl_map)
    else:
        raise ValueError(f'{mode}: Invalid "mode" value')

    if output is None:
        return None
    elif behavior == "exception":
        output = "\n    ".join(output)
        raise ValueError(f"Invalid {mode}-skeleton:\n    {output}")
    elif behavior == "report":
        return output
    else:
        raise ValueError(f'{behavior}: Invalid "behavior" value')


def _SingleSkeletonMapIssues(skl_map: array_t, /) -> list[str] | None:
    """Returns a list of invalid properties, if any, of the passed map when expecting a skeleton with a single connected
    component.

    Parameters
    ----------
    skl_map : numpy.ndarray

    Returns
    -------
    list[str], optional

    """
    output = _MultiSkeletonMapIssues(skl_map)
    if output is None:
        output = []

    _, n_components = tymp.LABELING_FCT_FOR_DIM[skl_map.ndim](skl_map)
    if n_components > 1:
        output.append(
            f"{n_components}: Too many connected components in map; Expected: 1"
        )

    if (output is None) or (output.__len__() == 0):
        return None
    return output


def _MultiSkeletonMapIssues(skl_map: array_t, /) -> list[str] | None:
    """Returns a list of invalid properties, if any, of the passed map when expecting a skeleton with one or more
    connected components.

    Parameters
    ----------
    skl_map : numpy.ndarray

    Returns
    -------
    list[str], optional

    """
    output = []

    if nmpy.issubdtype(skl_map.dtype, nmpy.floating):
        output.append(
            f"{skl_map.dtype}: Invalid map dtype; Expected: {nmpy.bool} or variants of {nmpy.integer}"
        )

    if skl_map.ndim not in (2, 3):
        output.append(f"{skl_map.ndim}: Invalid map dimension; Expected: 2 or 3")

    unique_values = nmpy.unique(skl_map)
    if not nmpy.array_equal(unique_values, (0, 1)):
        output.append(
            f"{unique_values}: Too many unique values in map; Expected: 0 and 1"
        )

    if (output is None) or (output.__len__() == 0):
        return None
    return output
