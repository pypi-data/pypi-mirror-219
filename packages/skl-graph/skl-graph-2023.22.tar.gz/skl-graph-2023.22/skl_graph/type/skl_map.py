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
Skeleton Map Creation and Manipulation.

Definitions
-----------
A map is a Numpy ndarray representing one or several object over a background. It exists in several variants:
- Boolean  map: ndarray of type bool            where the object(s) are labeled True and the background is False.
- Binary   map: ndarray of type int8  or uint8  where the object(s) are labeled 1 and the background is 0.
- Labeled  map: ndarray of type int64 or uint64 where the objects   are labeled from 1 with successive integers,
and the background is 0.
- Topology map: ndarray of type int8  or uint8  where each object site (pixel, voxel...) has a value between 0 and
3^D - 1, where D is the number of dimensions of the array, and the background is 3^D. The values correspond to the
number of neighboring sites belonging to the object with the weakest connectivity (8 in 2-D, 26 in 3-D...).

These variants are abbreviated omp, ymp, lmp, and tmp, respectively, to be used as a variable name postfix, e.g.,
edge_ymp.

For maps that can be of signed or unsigned types, the signed version is usually preferred to make them subtractable.

A skeleton map, normally abbreviated as skl_map, is a 2- or 3-dimensional boolean or binary map in which no site (pixel
or voxel) with value True, respectively 1, can be set to False, respectively 0, without breaking the skeleton
connectivity (in the weakest sense) or shortening a branch.

Simple example usage:
>>> # --- Object
>>> import skimage.data as data
>>> import skimage.util as util
>>> object_map = util.invert(data.horse())
>>> # --- SKL Map
>>> from skl_graph.type.skl_map import SKLMapFromObjectMap, PruneSKLMapBasedOnWidth
>>> skl_map, width_map = SKLMapFromObjectMap(object_map, with_width=True)
>>> pruned_map = skl_map.copy()
>>> PruneSKLMapBasedOnWidth(pruned_map, width_map, 20)
>>> # --- Plotting
>>> import matplotlib.pyplot as pyplot
>>> _, all_axes = pyplot.subplots(ncols=4)
>>> all_axes[0].matshow(object_map, cmap="gray")
>>> all_axes[1].matshow(skl_map, cmap="gray")
>>> all_axes[2].matshow(width_map, cmap="hot")
>>> all_axes[3].matshow(pruned_map, cmap="gray")
>>> for axes, title in zip(all_axes, ("Object", "Skeleton", "Width", "Pruned Skeleton")):
>>>     axes.set_title(title)
>>>     axes.set_axis_off()
>>> pyplot.tight_layout()
>>> pyplot.show()
"""

import numpy as nmpy
import scipy.ndimage as spim
import skimage.morphology as skmp

import skl_graph.type.tpy_map as tymp

array_t = nmpy.ndarray


def SKLMapFromObjectMap(
    object_map: array_t, /, *, with_width: bool = False
) -> array_t | tuple[array_t, array_t]:
    """Returns the skeleton map of an object map, optionally with the width map (see `SkeletonWidthMapFromObjectMap`).

    Works for multiple objects if skmp.thin and skmp.skeletonize_3d do.

    Parameters
    ----------
    object_map : numpy.ndarray
    with_width : bool

    Returns
    -------
    array_t | tuple[array_t, array_t]

    """
    if object_map.ndim == 2:
        # Documentation says it removes every pixel up to breaking connectivity
        Skeletonized = skmp.thin
    elif object_map.ndim == 3:
        # Documentation does not tell anything about every pixel being necessary or not
        Skeletonized = skmp.skeletonize_3d
    else:
        raise ValueError(f"{object_map.ndim}: Invalid map dimension; Expected: 2 or 3")

    skl_map = Skeletonized(object_map).astype(nmpy.bool_, copy=False)
    if object_map.ndim == 3:
        SKLMapFromThickVersion(skl_map, in_place=True)

    if with_width:
        return skl_map, SkeletonWidthMapFromObjectMap(object_map)
    return skl_map


def SkeletonWidthMapFromObjectMap(object_map: array_t, /) -> array_t:
    """Width map of an object map.

    The width map is a distance map where the values on the object(s) skeleton are equal to twice the distance to the
    object border, which can be interpreted as the local object width.

    Parameters
    ----------
    object_map : numpy.ndarray

    Returns
    -------
    numpy.ndarray

    """
    return 2.0 * spim.distance_transform_edt(object_map) + 1.0


_CENTER_3x3 = ((0, 0, 0), (0, 1, 0), (0, 0, 0))
_CROSS_3x3 = nmpy.array(((0, 1, 0), (1, 1, 1), (0, 1, 0)), dtype=nmpy.uint8)
_CROSS_3x3x3 = nmpy.array((_CENTER_3x3, _CROSS_3x3, _CENTER_3x3), dtype=nmpy.uint8)
_CROSS_FOR_DIM = (None, None, _CROSS_3x3, _CROSS_3x3x3)


def SKLMapFromThickVersion(
    skl_map: array_t, /, *, in_place: bool = False, should_only_check: bool = False
) -> array_t | bool | None:
    """Removes all sites (pixels or voxels) that do not break the skeleton connectivity (in the weakest sense) or
    shorten a branch.

    Works for multi-skeletons.
    """
    dtype = skl_map.dtype
    is_boolean = nmpy.issubdtype(dtype, nmpy.bool_)
    if not (is_boolean or nmpy.issubdtype(dtype, nmpy.integer)):
        raise ValueError(
            f"{dtype.name}: Invalid Numpy dtype. Expected=bool_ or integer-like."
        )

    if is_boolean:
        min_value = False
        max_value = True
    else:
        unique_values = nmpy.unique(skl_map)
        if (unique_values[0] != 0) or (unique_values.size != 2):
            raise ValueError(
                f"{unique_values}: Invalid unique values. Expected=0 and a strictly positive value."
            )
        min_value, max_value = unique_values

    skl_dimension = skl_map.ndim
    background_label = tymp.TMapBackgroundLabel(skl_map)
    patch_center = skl_dimension * (1,)
    cross = _CROSS_FOR_DIM[skl_dimension]
    padded_thinned = nmpy.pad(skl_map, 1)
    LabeledMap = tymp.LABELING_FCT_FOR_DIM[skl_dimension]

    def _DoFixPatches(
        _tpy_map: array_t,
        _n_neighbors: int,
        /,
    ) -> bool:
        """"""
        _skel_has_been_modified = False

        for where in zip(*nmpy.where(_tpy_map == _n_neighbors)):
            patch_slices = tuple(slice(coord - 1, coord + 2) for coord in where)
            tpy_patch = _tpy_map[patch_slices]
            if nmpy.any(tpy_patch[cross] == background_label):
                patch = padded_thinned[patch_slices]
                patch[patch_center] = min_value

                _, n_components = LabeledMap(patch)
                if n_components == 1:
                    _skel_has_been_modified = True
                else:
                    patch[patch_center] = max_value

        return _skel_has_been_modified

    def _JustCheckPatches(
        _tpy_map: array_t,
        _n_neighbors: int,
        /,
    ) -> bool:
        """"""
        for where in zip(*nmpy.where(_tpy_map == _n_neighbors)):
            patch_slices = tuple(slice(coord - 1, coord + 2) for coord in where)
            tpy_patch = _tpy_map[patch_slices]
            if nmpy.any(tpy_patch[cross] == background_label):
                patch = padded_thinned[patch_slices]
                patch[patch_center] = min_value

                _, n_components = LabeledMap(patch)
                if n_components == 1:
                    return True
                else:
                    patch[patch_center] = max_value

        return False

    if should_only_check:
        _FixPatches = _JustCheckPatches
    else:
        _FixPatches = _DoFixPatches
    excluded_n_neighbors = {
        0,
        1,
        2 * skl_dimension,
        background_label,
    }
    skel_has_been_modified = True
    while skel_has_been_modified:
        skel_has_been_modified = False

        tpy_map = tymp.TopologyMapOfMap(padded_thinned, full_connectivity=False)
        included_n_neighbors = set(nmpy.unique(tpy_map)).difference(
            excluded_n_neighbors
        )

        for n_neighbors in sorted(included_n_neighbors, reverse=True):
            skel_has_been_modified = skel_has_been_modified or _FixPatches(
                tpy_map,
                n_neighbors,
            )
            if should_only_check and skel_has_been_modified:
                return False

    if should_only_check:
        return True

    if skl_dimension == 2:
        thinned = padded_thinned[1:-1, 1:-1]
    else:
        thinned = padded_thinned[1:-1, 1:-1, 1:-1]

    if in_place:
        nmpy.copyto(skl_map, thinned)
    else:
        return thinned


def PruneSKLMapBasedOnWidth(
    skl_map: array_t, width_map: array_t, min_width: float, /
) -> None:
    """Prunes the skeleton map so that the resulting skeleton corresponds everywhere to object portions wider than the
    passed minimal width.

    Works for multi-skeletons.

    Parameters
    ----------
    skl_map : numpy.ndarray
    width_map : numpy.ndarray
    min_width : float

    Returns
    -------
    None

    """
    while True:
        tpy_map = tymp.TopologyMapOfMap(skl_map)
        end_positions = nmpy.where(tpy_map == 1)
        distances = width_map[end_positions]

        tiny_distances = distances < min_width
        if tiny_distances.any():
            extra_positions = tuple(site[tiny_distances] for site in end_positions)
            skl_map[extra_positions] = 0
        else:
            break
