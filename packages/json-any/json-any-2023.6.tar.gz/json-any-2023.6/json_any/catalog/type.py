# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2022)
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

from array import array as py_array_t
from datetime import date as date_t
from datetime import datetime as date_time_t
from datetime import time as time_t
from datetime import timedelta as time_delta_t
from datetime import timezone as time_zone_t
from enum import Enum as enum_t
from io import BytesIO as io_bytes_t
from pathlib import PurePath as path_t
from typing import NamedTuple as named_tuple_t
from typing import Any, Sequence
from uuid import UUID as uuid_t

from json_any.catalog.module import grph, nmpy, pnds, pypl, sprs
from json_any.constant import MODULE_TYPE_SEPARATOR

BUILTIN_BYTES_CONTAINERS = (bytes, bytearray)
BUILTIN_CONTAINERS = (frozenset, list, set, tuple)
JSON_TYPE: dict[type, str] = {}  # Matches non-builtin types with module-name_type-name.
JSON_TYPE_NUMPY_SCALAR = f"{nmpy.__name__}{MODULE_TYPE_SEPARATOR}SCALAR"
JSON_TYPE_PREFIX_PATHLIB = f"{path_t.__module__}{MODULE_TYPE_SEPARATOR}"

BUILTIN_BYTES_CONTAINERS_NAMES = tuple(
    _tpe.__name__ for _tpe in BUILTIN_BYTES_CONTAINERS
)
BUILTIN_CONTAINERS_NAMES = tuple(_tpe.__name__ for _tpe in BUILTIN_CONTAINERS)


def ContainerWithName(name: str, /) -> type:
    """"""
    if name in BUILTIN_BYTES_CONTAINERS_NAMES:
        return BUILTIN_BYTES_CONTAINERS[BUILTIN_BYTES_CONTAINERS_NAMES.index(name)]
    else:
        return BUILTIN_CONTAINERS[BUILTIN_CONTAINERS_NAMES.index(name)]


def TypeIsInModule(json_type: str, module: Any, /) -> bool:
    """"""
    module_name = module.__name__
    return json_type.startswith(module_name) and (
        json_type[module_name.__len__()] in (".", MODULE_TYPE_SEPARATOR)
    )


def TypeNameOf(json_type: str, /) -> str:
    """"""
    return json_type[(json_type.rindex(MODULE_TYPE_SEPARATOR) + 1) :]


def _AddJsonTypes(types: Sequence[type], /) -> None:
    """"""
    global JSON_TYPE

    for type_ in types:
        JSON_TYPE[type_] = f"{type_.__module__}{MODULE_TYPE_SEPARATOR}{type_.__name__}"


_AddJsonTypes(
    (
        date_t,
        date_time_t,
        enum_t,
        io_bytes_t,
        named_tuple_t,
        py_array_t,
        time_delta_t,
        time_t,
        time_zone_t,
        uuid_t,
    )
)


# Note: When there is a single class of interest in a module, the purpose of a *_CLASSES
# tuple is to have an homogeneous dealing of all modules.

if pypl is None:
    MATPLOTLIB_CLASSES = ()
else:
    figure_t = pypl.Figure
    MATPLOTLIB_CLASSES = (figure_t,)
    # Unfortunately, figure_t.__nodule__ is reported as "matplotlib.figure" instead of
    # the expected "matplotlib.pyplot".
    JSON_TYPE[figure_t] = f"{pypl.__name__}{MODULE_TYPE_SEPARATOR}{figure_t.__name__}"

if grph is None:
    NETWORKX_CLASSES = ()
else:
    NETWORKX_CLASSES = (grph.Graph, grph.DiGraph, grph.MultiGraph, grph.MultiDiGraph)
    _AddJsonTypes(NETWORKX_CLASSES)

if nmpy is None:
    np_array_t = None
    NUMPY_ARRAY_CLASSES = ()
else:
    np_array_t = nmpy.ndarray
    NUMPY_ARRAY_CLASSES = (np_array_t,)
    _AddJsonTypes(NUMPY_ARRAY_CLASSES)

if pnds is None:
    PANDAS_CLASSES = ()
else:
    PANDAS_CLASSES = (pnds.Series, pnds.DataFrame)
    _AddJsonTypes(PANDAS_CLASSES)

if sprs is None:
    SCIPY_ARRAY_CLASSES = ()
else:
    SCIPY_ARRAY_CLASSES = (
        sprs.bsr_array,
        sprs.coo_array,
        sprs.csc_array,
        sprs.csr_array,
        sprs.dia_array,
        sprs.dok_array,
        sprs.lil_array,
    )
    _AddJsonTypes(SCIPY_ARRAY_CLASSES)
