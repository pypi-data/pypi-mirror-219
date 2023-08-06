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

from json_any.catalog.type import (
    array_t,
    data_frame_t,
    date_t,
    date_time_t,
    enum_t,
    figure_t,
    io_bytes_t,
    named_tuple_t,
    py_array_t,
    series_t,
    time_delta_t,
    time_t,
    time_zone_t,
    uuid_t,
)

JSONING_ERROR_MARKER = "/!\\"

DESCRIPTION_FOR_JSON = "__DescriptionForJSON__"
NEW_FROM_JSON_DESCRIPTION = "__NewFromJsonDescription__"

CUSTOM_PREFIX = "CUSTOM_"
DATACLASS_PREFIX = "DATACLASS_"
STANDARD_PREFIX = "STANDARD_"
UNHANDLED_PREFIX = "UNHANDLED_"

JSON_TYPE_PREFIX_NETWORKX = "networkx_"
JSON_TYPE_PREFIX_PANDAS = "pandas_"
JSON_TYPE_PREFIX_PATHLIB = "pathlib_"
JSON_TYPE_PREFIX_SCIPY = "scipy_"
# For data_frame_t and series_t, use "frame" and "series" as postfixes since it is used
# for pandas.read_json's "typ" parameter.
JSON_TYPE = {
    array_t: "numpy_ndarray",
    data_frame_t: f"{JSON_TYPE_PREFIX_PANDAS}frame",
    date_t: "datetime_date",
    date_time_t: "datetime_datetime",
    enum_t: "enum_Enum_",
    figure_t: "matplotlib_pyplot_Figure",
    io_bytes_t: "io_BytesIO",
    named_tuple_t: "typing_NamedTuple_",
    py_array_t: "array_array",
    series_t: f"{JSON_TYPE_PREFIX_PANDAS}series",
    time_delta_t: "datetime_timedelta",
    time_t: "datetime_time",
    time_zone_t: "datetime_timezone",
    uuid_t: "uuid_UUID",
}
JSON_TYPE_NUMPY_SCALAR = "numpy_scalar"
