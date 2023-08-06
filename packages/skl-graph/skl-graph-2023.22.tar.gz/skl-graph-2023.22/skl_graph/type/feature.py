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

from typing import NamedTuple as named_tuple_t

import numpy as nmpy

array_t = nmpy.ndarray


class lengths_t(named_tuple_t):
    """
    segment_: prefix for pixel-to-pixel segments
    segment_sq_lengths: squared segment lengths; Interest: all integers
    """

    length: float
    segment_lengths: array_t
    segment_sq_lengths: array_t

    @classmethod
    def NewFromSites(cls, sites: tuple[array_t, ...], /) -> lengths_t:
        """"""
        sites_as_array = nmpy.array(sites)
        segments = nmpy.diff(sites_as_array, axis=1)
        segment_sq_lengths = nmpy.sum(segments**2, axis=0)
        segment_lengths = nmpy.sqrt(segment_sq_lengths)
        length = segment_lengths.sum().item()

        return cls(
            length=length,
            segment_lengths=segment_lengths,
            segment_sq_lengths=segment_sq_lengths,
        )


class areas_t(named_tuple_t):
    """
    segment_: prefix for pixel-to-pixel segments
    segment_based_area: width-weighted length
    """

    mean_width: float
    mean_based_area: float | None
    segment_based_area: float | None

    @classmethod
    def NewFromLengthsAndWidths(
        cls,
        lengths: lengths_t,
        widths: array_t,
        /,
    ) -> areas_t:
        """"""
        mean_width = nmpy.mean(widths).item()
        mean_based_area = lengths.length * mean_width
        segment_based_area = (
            (0.5 * (widths[1:] + widths[:-1]) * lengths.segment_lengths).sum().item()
        )

        return cls(
            mean_width=mean_width,
            mean_based_area=mean_based_area,
            segment_based_area=segment_based_area,
        )
