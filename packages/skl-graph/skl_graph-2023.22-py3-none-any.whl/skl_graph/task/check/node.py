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

from skl_graph.extension.numpy_ import Issues as NumpyArrayIssues
from skl_graph.type.node import branch_node_t, end_node_t

array_t = nmpy.ndarray


def Issues(node: end_node_t | branch_node_t, /) -> Sequence[str]:
    """"""
    output = []

    issues = NumpyArrayIssues(
        node.position,
        expected_dtype=nmpy.integer,
        expected_size=(2, 3),
        expected_shape=((2,), (3,)),
    )
    if issues.__len__() > 0:
        issues = ("Node position: " + _iss for _iss in issues)
        output.extend(issues)
        expected_dim = None
    else:
        expected_dim = node.position.size

    if node.uid is None:
        output.append("Node without UID")

    if isinstance(node, branch_node_t):
        if isinstance(node.sites, tuple) and (node.sites.__len__() in (2, 3)):
            if (expected_dim is None) or (node.sites.__len__() == expected_dim):
                if all(isinstance(_elm, array_t) for _elm in node.sites):
                    expected_size = node.sites[0].size
                    expected_shape = (expected_size,)
                    for c_idx, component in enumerate(node.sites):
                        issues = NumpyArrayIssues(
                            component,
                            expected_dtype=nmpy.integer,
                            expected_size=expected_size,
                            expected_shape=expected_shape,
                        )
                        if issues.__len__() > 0:
                            issues = (f"Node sites[{c_idx}]: {_iss}" for _iss in issues)
                            output.extend(issues)
                else:
                    output.append(
                        f"{tuple(type(_elm).__name__ for _elm in node.sites)}: "
                        f"Invalid type(s) of node sites components. "
                        f"Expected=all {array_t.__name__}'s."
                    )
            else:
                output.append(
                    f"{node.sites.__len__()}: Invalid node sites dimension. "
                    f"Expected={expected_dim}."
                )
        else:
            if isinstance(node.sites, Sequence):
                dimension = node.sites.__len__()
            else:
                dimension = "N/A"
            output.append(
                f"T:{type(node.sites).__name__}, D:{dimension}: "
                f"Invalid type T or dimension D of node sites. "
                f"Expected=tuple with 2 or 3 elements."
            )

    return output
