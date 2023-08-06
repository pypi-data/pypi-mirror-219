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
from uuid import UUID as uuid_t

from json_any.catalog.module import grph, nmpy, pnds, pypl, sprs

# When a module is not found, using bytes, the first type tested while JSONing, as the main module type is a safe way to
# "disable" it.
if pypl is None:
    figure_t = bytes
else:
    figure_t = pypl.Figure
if grph is None:
    NX_GRAPH_CLASSES = bytes
else:
    NX_GRAPH_CLASSES = (grph.Graph, grph.DiGraph, grph.MultiGraph, grph.MultiDiGraph)
if nmpy is None:
    array_t = bytes
else:
    array_t = nmpy.ndarray
if pnds is None:
    series_t = data_frame_t = bytes
else:
    series_t = pnds.Series
    data_frame_t = pnds.DataFrame
if sprs is None:
    SPARSE_ARRAY_CLASSES = bytes
else:
    SPARSE_ARRAY_CLASSES = (
        sprs.bsr_array,
        sprs.coo_array,
        sprs.csc_array,
        sprs.csr_array,
        sprs.dia_array,
        sprs.dok_array,
        sprs.lil_array,
    )
