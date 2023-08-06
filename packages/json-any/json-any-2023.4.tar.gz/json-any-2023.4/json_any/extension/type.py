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

import dataclasses as dtcl
import importlib as imlb
import sys as sstm
from types import GenericAlias
from typing import Any, Callable, Union, get_origin

from json_any.catalog.type import enum_t

builders_h = dict[str, Callable[[Any], Any]]
description_h = tuple[str, Any]
descriptors_h = dict[str, Callable[[Any], Any]]


_MODULE_SEPARATOR = ":"  # Must be a character forbidden in any (qualified) name


class unfound_t:
    pass


def FullyQualifiedType(instance_or_type: Union[Any, type], /) -> str:
    """"""
    # TODO: Explain why an enum_t instance must not be processed by TypeOfInstance.
    if (type(instance_or_type) is type) or issubclass(instance_or_type, enum_t):
        type_ = instance_or_type
    else:
        type_ = TypeOfInstance(instance_or_type)

    return f"{type_.__module__}{_MODULE_SEPARATOR}{type_.__name__}"


def TypeFromJsonType(
    json_type: str, /, *, prefix: str = "", should_continue_on_error: bool = False
) -> type:
    """"""
    module, type_ = json_type[prefix.__len__() :].split(_MODULE_SEPARATOR, maxsplit=1)
    error = None

    imported = sstm.modules.get(module, None)
    if imported is None:
        # Do not put instead of "None" in "get" above since it will then be evaluated
        # all the time, I suppose.
        try:
            imported = imlb.import_module(module)
        except ModuleNotFoundError:
            error = f'{module}: Module not found when looking for type "{type_}".'

    if imported is None:
        output = None
    else:
        try:
            output = getattr(imported, type_)
        except AttributeError:
            output = None
            error = f'{type_}: Type not found in module "{module}".'

    if output is None:
        if should_continue_on_error:
            output = unfound_t
        else:
            raise TypeError(error)

    return output


def TypeOfInstance(instance: Any, /) -> type:
    """"""
    if isinstance(instance, GenericAlias):
        return get_origin(type(instance))

    return type(instance)


def IsNamedTuple(instance: Any, /) -> bool:
    """"""
    instance_type = TypeOfInstance(instance)
    if hasattr(instance_type, "_make"):
        try:
            as_tuple = tuple(instance)
        except TypeError:
            return False

        return instance_type._make(as_tuple) == instance

    return False


def IsFullyDataclassBased(instance_type: type, /) -> bool:
    """"""
    if dtcl.is_dataclass(instance_type):
        inheritance = instance_type.__mro__[1:]  # Exclude oneself
        if inheritance[0] is object:
            return True

        # Exclude object
        return all(IsFullyDataclassBased(_typ) for _typ in inheritance[:-1])

    return False
