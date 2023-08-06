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

from io import BytesIO as bytes_io_t
from io import StringIO as string_io_t
from pathlib import Path as path_t
from typing import Any, Callable, Sequence

from json_any.extension.type import builders_h, descriptors_h
from json_any.json_to_object import ObjectFromJsonString
from json_any.object_to_json import JsonStringOf
from json_any.task.compression import (
    STANDARD_COMPRESSOR_MODULES,
    CompressedVersion,
    DecompressedVersion,
)


def StoreAsJSON(
    instance: Any,
    path: str | path_t | bytes_io_t | string_io_t,
    /,
    *args,
    descriptors: descriptors_h = None,
    compressor: str
    | Callable[[bytes, ...], bytes]
    | None = STANDARD_COMPRESSOR_MODULES[0],
    should_continue_on_error: bool = False,
    should_overwrite_path: bool = False,
    **kwargs,
) -> Sequence[str] | None:
    """"""
    if isinstance(path, str):
        path = path_t(path)
    if (
        isinstance(path, path_t)
        and path.exists()
        and not (path.is_file() and should_overwrite_path)
    ):
        raise ValueError(
            f"{path}: Path exists and is not a file or should not be overwritten."
        )
    if (isinstance(path, bytes_io_t) and (compressor is None)) or (
        isinstance(path, string_io_t) and (compressor is not None)
    ):
        raise ValueError(
            f"T.{type(path).__name__}, C.{compressor}: Path-like type T and "
            f"compression C mismatch. Expected={bytes_io_t} with compression, "
            f"or {string_io_t} without compression."
        )

    jsoned, history = JsonStringOf(instance, descriptors=descriptors)
    if history is None:
        if compressor is None:
            content = jsoned
            mode = "w"
        else:
            content = CompressedVersion(jsoned, *args, compressor=compressor, **kwargs)
            mode = "wb"
        if isinstance(path, path_t):
            with open(path, mode=mode) as json_accessor:
                json_accessor.write(content)
        else:
            path.write(content)
    elif should_continue_on_error:
        return history
    else:
        raise RuntimeError("\n".join(history))


def LoadFromJSON(
    path: str | path_t | bytes_io_t | string_io_t,
    /,
    *args,
    builders: builders_h = None,
    decompressor: str
    | Callable[[bytes, ...], bytes]
    | None = STANDARD_COMPRESSOR_MODULES[0],
    should_continue_on_error: bool = False,
    **kwargs,
) -> Any:
    """"""
    if isinstance(path, (str, path_t)):
        if decompressor is None:
            mode = "r"
        else:
            mode = "rb"
        with open(path, mode=mode) as json_accessor:
            content = json_accessor.read()
    else:
        if (isinstance(path, bytes_io_t) and (decompressor is None)) or (
            isinstance(path, string_io_t) and (decompressor is not None)
        ):
            raise ValueError(
                f"T.{type(path).__name__}, D.{decompressor}: Path-like type T and "
                f"decompression D mismatch. Expected={bytes_io_t} with decompression, "
                f"or {string_io_t} without decompression."
            )
        content = path.read()

    if decompressor is None:
        jsoned = content
    else:
        jsoned = DecompressedVersion(
            content,
            *args,
            decompressor=decompressor,
            **kwargs,
        )

    return ObjectFromJsonString(
        jsoned,
        builders=builders,
        should_continue_on_error=should_continue_on_error,
    )
