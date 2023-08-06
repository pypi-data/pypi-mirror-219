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
import json
import pathlib as pthl
from typing import Any

from json_any.catalog.module import grph, nmpy, pnds, pypl, sprs
from json_any.catalog.type import (
    BUILTIN_BYTES_CONTAINERS_NAMES,
    BUILTIN_CONTAINERS_NAMES,
    JSON_TYPE,
    JSON_TYPE_NUMPY_SCALAR,
    JSON_TYPE_PREFIX_PATHLIB,
    ContainerWithName,
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
from json_any.constant import (
    CUSTOM_PREFIX,
    DATACLASS_PREFIX,
    MODULE_TYPE_SEPARATOR,
    NEW_FROM_JSON_DESCRIPTION,
    STANDARD_PREFIX,
    UNHANDLED_PREFIX,
)
from json_any.extension.numpy import AsNumpyArray
from json_any.extension.type import (
    TypeFromJsonType,
    builders_h,
    description_h,
    unfound_t,
)


def ObjectFromJsonString(
    jsoned: str,
    /,
    *,
    builders: builders_h = None,
    should_continue_on_error: bool = False,
) -> Any:
    """"""
    return _ObjectFromUnJSONed(
        json.loads(jsoned),
        highest_level_call=True,
        builders=builders,
        should_continue_on_error=should_continue_on_error,
    )


def _ObjectFromUnJSONed(
    description: description_h,
    /,
    *,
    highest_level_call: bool = False,
    builders: builders_h = None,
    should_continue_on_error: bool = False,
) -> Any:
    """"""
    json_type, instance = description
    if json_type.startswith(UNHANDLED_PREFIX):
        print(
            f"{json_type[UNHANDLED_PREFIX.__len__():]}: UnJSONable type. Returning None."
        )
        return None

    if builders is None:
        builders = {}

    if json_type.startswith(CUSTOM_PREFIX):
        fully_qualified = json_type[CUSTOM_PREFIX.__len__() :]
        if fully_qualified in builders:
            Rebuilt = builders[fully_qualified]
        elif highest_level_call and ("" in builders):
            Rebuilt = builders[""]
        else:
            output_t = TypeFromJsonType(
                fully_qualified, should_continue_on_error=should_continue_on_error
            )
            Rebuilt = getattr(output_t, NEW_FROM_JSON_DESCRIPTION, None)
        if Rebuilt is None:
            output = None
            print(f"{json_type}: Unfound type or type without builder. Returning None.")
        else:
            output = Rebuilt(
                _ObjectFromUnJSONed(
                    instance,
                    builders=builders,
                    should_continue_on_error=should_continue_on_error,
                )
            )
    elif json_type.startswith(DATACLASS_PREFIX):
        output_t = TypeFromJsonType(
            json_type,
            prefix=DATACLASS_PREFIX,
            should_continue_on_error=should_continue_on_error,
        )
        if output_t is unfound_t:
            output = None
            print(f"{json_type}: Unfound type. Returning None.")
        else:
            as_dict = _ObjectFromUnJSONed(
                instance,
                builders=builders,
                should_continue_on_error=should_continue_on_error,
            )

            for_init = {}
            for field in dtcl.fields(output_t):
                if field.init:
                    # This could be limited to init fields without default values. However, all kind of things can happen in
                    # init or post_init, so hopefully, the choice to ignore default values here works...
                    name = field.name
                    for_init[name] = as_dict[name]
            output = output_t(**for_init)
            # Despite initial values being passed above, all the fields are reset here to their values at JSONing time,
            # again in case things happen in init or post_init.
            for key, value in as_dict.items():
                setattr(output, key, value)
    elif json_type in BUILTIN_BYTES_CONTAINERS_NAMES:
        output_t = ContainerWithName(json_type)
        output = instance.encode(encoding="iso-8859-1")
        if type(output) is not output_t:
            # In practice, this is only for bytearray since bytes are already bytes.
            output = output_t(output)
    elif json_type == complex.__name__:
        output = complex(*instance)
    elif json_type == slice.__name__:
        output = slice(*instance)
    elif json_type == JSON_TYPE[uuid_t]:
        output = uuid_t(int=instance)
    elif json_type == JSON_TYPE[date_t]:
        output = date_t(*instance)
    elif json_type == JSON_TYPE[time_delta_t]:
        output = time_delta_t(*instance)
    elif json_type == JSON_TYPE[py_array_t]:
        as_list, typecode = instance
        output = py_array_t(typecode)
        output.fromlist(as_list)
    elif json_type == JSON_TYPE[io_bytes_t]:
        output = io_bytes_t(instance.encode(encoding="iso-8859-1"))
    elif json_type.startswith(JSON_TYPE_PREFIX_PATHLIB):
        type_name = json_type[JSON_TYPE_PREFIX_PATHLIB.__len__() :]
        output_t = getattr(pthl, type_name)
        output = output_t(instance)
    elif TypeIsInModule(json_type, sprs):
        type_name = TypeNameOf(json_type)
        output_t = getattr(sprs, type_name)
        output = output_t(AsNumpyArray(*instance))
    elif (json_type != JSON_TYPE_NUMPY_SCALAR) and TypeIsInModule(json_type, nmpy):
        output = AsNumpyArray(*instance)
    elif TypeIsInModule(json_type, pnds):
        type_name = TypeNameOf(json_type)
        as_dict = _ObjectFromUnJSONed(
            instance,
            builders=builders,
            should_continue_on_error=should_continue_on_error,
        )
        output_t = getattr(pnds, type_name)
        output = output_t(as_dict)
    elif json_type == JSON_TYPE_NUMPY_SCALAR:
        dtype, value = instance
        if isinstance(value, list):
            output = nmpy.dtype(dtype).type(complex(*value))
        else:
            output = nmpy.dtype(dtype).type(value)
    elif TypeIsInModule(json_type, pypl):
        fake_file = io_bytes_t(instance.encode(encoding="iso-8859-1"))
        image = pypl.imread(fake_file)
        fake_file.close()
        output, axes = pypl.subplots()
        axes.set_axis_off()
        axes.matshow(image)
    elif json_type == JSON_TYPE[date_time_t]:
        date, time = _ObjectFromUnJSONed(instance)
        output = date_time_t(
            date.year,
            date.month,
            date.day,
            time.hour,
            time.minute,
            time.second,
            time.microsecond,
            time.tzinfo,
            fold=time.fold,
        )
    elif json_type == JSON_TYPE[time_t]:
        time_zone = _ObjectFromUnJSONed(instance[4])
        as_dict = dict(
            zip(
                ("hour", "minute", "second", "microsecond", "tzinfo", "fold"),
                (*instance[:4], time_zone, *instance[5:]),
            )
        )
        output = time_t(**as_dict)
    elif json_type == JSON_TYPE[time_zone_t]:
        time_delta, name = _ObjectFromUnJSONed(instance)
        output = time_zone_t(time_delta, name=name)
    elif json_type.startswith(JSON_TYPE[enum_t]):
        output_t = TypeFromJsonType(
            json_type,
            prefix=JSON_TYPE[enum_t],
            should_continue_on_error=should_continue_on_error,
        )
        if output_t is unfound_t:
            output = None
            print(f"{json_type}: Unfound type. Returning None.")
        else:
            output = output_t(
                _ObjectFromUnJSONed(
                    instance,
                    builders=builders,
                    should_continue_on_error=should_continue_on_error,
                )
            )
    elif json_type.startswith(JSON_TYPE[named_tuple_t]):
        output_t = TypeFromJsonType(
            json_type,
            prefix=JSON_TYPE[named_tuple_t],
            should_continue_on_error=should_continue_on_error,
        )
        if output_t is unfound_t:
            output = None
            print(f"{json_type}: Unfound type. Returning None.")
        else:
            output = output_t._make(
                _ObjectFromUnJSONed(
                    instance,
                    builders=builders,
                    should_continue_on_error=should_continue_on_error,
                )
            )
    elif json_type in BUILTIN_CONTAINERS_NAMES:
        iterator = (
            _ObjectFromUnJSONed(
                _elm,
                builders=builders,
                should_continue_on_error=should_continue_on_error,
            )
            for _elm in instance
        )
        output_t = ContainerWithName(json_type)
        output = output_t(iterator)
    elif json_type == dict.__name__:
        output = {
            _ObjectFromUnJSONed(
                json.loads(_key),
                builders=builders,
                should_continue_on_error=should_continue_on_error,
            ): _ObjectFromUnJSONed(
                _vle,
                builders=builders,
                should_continue_on_error=should_continue_on_error,
            )
            for _key, _vle in instance.items()
        }
    elif TypeIsInModule(json_type, grph):
        type_name = TypeNameOf(json_type)
        output_t = getattr(grph, type_name)

        edges_w_attributes = _ObjectFromUnJSONed(
            instance,
            builders=builders,
            should_continue_on_error=should_continue_on_error,
        )
        attributes = {}
        edges = {}
        for node, (node_attributes, edge) in edges_w_attributes.items():
            attributes[node] = node_attributes
            edges[node] = edge

        output = grph.from_dict_of_dicts(
            edges,
            create_using=output_t,
            multigraph_input=output_t in (grph.MultiGraph, grph.MultiDiGraph),
        )
        grph.set_node_attributes(output, attributes)
    elif json_type.startswith(STANDARD_PREFIX):
        output = instance
    else:
        raise ValueError(f"{json_type}: Invalid JSON type or error while unJSONing.")

    return output


def TypeIsInModule(json_type: str, module: Any, /) -> bool:
    """"""
    module_name = module.__name__
    return json_type.startswith(module_name) and (
        json_type[module_name.__len__()] in (".", MODULE_TYPE_SEPARATOR)
    )


def TypeNameOf(json_type: str, /) -> str:
    """"""
    return json_type[(json_type.rindex(MODULE_TYPE_SEPARATOR) + 1) :]
