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
from typing import Any, Callable, Sequence, NoReturn, Hashable

from json_any.extension.type import builders_h, descriptors_h
from json_any.json_to_object import ObjectFromJsonString
from json_any.object_to_json import JsonStringOf
from json_any.task.compression import (
    STANDARD_COMPRESSOR_MODULES,
    CompressedVersion,
    DecompressedVersion,
)

STANDARD_COMPRESSOR_EXTENSIONS = {
    None: ".json",
    "bz2": ".json.bz2",
    "gzip": ".json.gz",
    "lzma": ".json.lzma",
    "zlib": ".json.zlib",
}
DECOMPRESSOR_AUTO = "AUTO"


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
    should_add_standard_extension: bool = True,
    should_overwrite_path: bool = False,
    **kwargs,
) -> path_t | Sequence[str] | None:
    """"""
    if isinstance(path, str):
        path = path_t(path)

    if (
        isinstance(path, path_t)
        and isinstance(compressor, Hashable)
        and (compressor in STANDARD_COMPRESSOR_EXTENSIONS)
    ):
        extensions = path.suffixes
        if extensions.__len__() > 0:
            _CheckCompressorAndStdExtensionMatching(
                compressor, "compressor", extensions
            )
        elif should_add_standard_extension:
            path = path.with_suffix(STANDARD_COMPRESSOR_EXTENSIONS[compressor])

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
            return path
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
    decompressor: str | Callable[[bytes, ...], bytes] | None = DECOMPRESSOR_AUTO,
    should_continue_on_error: bool = False,
    **kwargs,
) -> Any:
    """"""
    if isinstance(path, str):
        path = path_t(path)

    if isinstance(path, path_t):
        extensions = path.suffixes
        if decompressor == DECOMPRESSOR_AUTO:
            if extensions.__len__() > 0:
                decompressor = _DecompressorFromExtension(extensions)
            else:
                raise ValueError(
                    f"{path.name}: Decompressor selection cannot be left to loader "
                    f"when loading from a path without extension."
                )
        elif (
            (extensions.__len__() > 0)
            and isinstance(decompressor, Hashable)
            and (decompressor in STANDARD_COMPRESSOR_EXTENSIONS)
        ):
            _CheckCompressorAndStdExtensionMatching(
                decompressor, "decompressor", extensions
            )

        if decompressor is None:
            mode = "r"
        else:
            mode = "rb"
        with open(path, mode=mode) as json_accessor:
            content = json_accessor.read()
    elif decompressor == DECOMPRESSOR_AUTO:
        raise ValueError(
            f"{decompressor}: Decompressor selection cannot be left to loader "
            f"when not loading from path."
        )
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


def _CheckCompressorAndStdExtensionMatching(
    compressor: Hashable, actual: str, extensions: Sequence[str], /
) -> None | NoReturn:
    """
    Actually, compressor or decompressor, with "actual" allowing to make the difference.
    """
    full_extension = "".join(extensions)
    found = False
    for (
        std_compressor,
        std_full_extension,
    ) in STANDARD_COMPRESSOR_EXTENSIONS.items():
        if full_extension.lower() == std_full_extension:
            found = compressor == std_compressor
            break

    if not found:
        initial = actual[0].upper()
        expected = " or ".join(
            f"{initial}.{_key}+E.{_vle}"
            for _key, _vle in STANDARD_COMPRESSOR_EXTENSIONS.items()
        )
        raise ValueError(
            f"{initial}.{compressor}, E.{full_extension}: {actual.capitalize()} "
            f"{initial} and extension E do not match. Expected={expected}."
        )


def _DecompressorFromExtension(extensions: Sequence[str], /) -> str | None | NoReturn:
    """"""
    full_extension = "".join(extensions)
    for (
        std_compressor,
        std_full_extension,
    ) in STANDARD_COMPRESSOR_EXTENSIONS.items():
        if full_extension.lower() == std_full_extension:
            return std_compressor

    expected = " or ".join(STANDARD_COMPRESSOR_EXTENSIONS.values())
    raise ValueError(
        f"{full_extension}: Not a valid extension for automatic decompressor "
        f"selection. Expected={expected}."
    )
