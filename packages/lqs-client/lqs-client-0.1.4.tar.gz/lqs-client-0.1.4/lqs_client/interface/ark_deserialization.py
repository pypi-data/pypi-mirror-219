from collections import OrderedDict
import sys
from .input_stream import InputStream
from typing import Callable, Dict, List, Optional


def read_enum(input_stream: InputStream, enum_name: str, schema_registry: dict):
    values = schema_registry["enums"][enum_name]["values"]
    type = schema_registry["enums"][enum_name]["enum_class"]
    accepted_types = [
        "uint64",
        "uint32",
        "uint16",
        "uint8",
        "int64",
        "int32",
        "int16",
        "int8",
    ]
    assert type in accepted_types, f"enum type must be one of {accepted_types}"
    method_name = f"read_{type}"
    read_fn = getattr(input_stream, method_name)
    value = read_fn()
    return values[value]


def get_read_fn(
    input_stream: InputStream,
    schema_registry: dict,
    field: dict,
    trim,
    trim_size,
):
    type_identifier = field["type"]
    # if its a simple type return the read function
    if type_identifier in [
        "bool",
        "int8",
        "uint8",
        "int16",
        "uint16",
        "int32",
        "uint32",
        "int64",
        "uint64",
        "double",
        "float",
        "string",
        "guid",
    ]:
        return getattr(input_stream, f"read_{type_identifier}")
    if type_identifier == "byte_buffer":
        return lambda: list(input_stream.read_byte_buffer())
    if type_identifier in ["steady_time_point", "system_time_point"]:
        return getattr(input_stream, "read_uint64")
    if type_identifier in ["duration"]:
        return getattr(input_stream, "read_int64")
    if type_identifier in ["enum"]:
        type_name = field["object_type"]
        return lambda: read_enum(
            input_stream, enum_name=type_name, schema_registry=schema_registry
        )
    if type_identifier in ["object"]:
        type_name = field["object_type"]
        read_fn = lambda: deserialize(  # noqa: E731
            input_stream,
            schema_registry,
            type_identifier=type_name,
            trim=trim,
            trim_size=trim_size,
        )

        def wrap():
            # we need to do this since we aren't using read_object which does this logic
            pushed_flags = input_stream.has_more_sections
            input_stream.has_more_sections = False
            res = read_fn()
            input_stream.has_more_sections = pushed_flags
            return res

        return wrap
    if type_identifier in ["arraylist"]:
        # TODO can improve performance for primitive types
        array_size = input_stream.read_array_size(None)
        element_read_func = get_read_fn(
            input_stream,
            schema_registry,
            field["ctr_value_type"],
            trim=trim,
            trim_size=trim_size,
        )
        read_fn = lambda: input_stream.read_array(  # noqa: E731
            read_fn=element_read_func, fixed_array_size=array_size
        )
        if trim and array_size >= trim_size:

            def read_and_ignore():
                read_fn()
                return None

            return read_and_ignore
        return read_fn
    if type_identifier in ["dictionary"]:
        key_type_fn = get_read_fn(
            input_stream,
            schema_registry,
            field["ctr_key_type"],
            trim=trim,
            trim_size=trim_size,
        )
        value_type_fn = get_read_fn(
            input_stream,
            schema_registry,
            field["ctr_value_type"],
            trim=trim,
            trim_size=trim_size,
        )
        dictionary_size = input_stream.read_array_size(None)
        if trim and dictionary_size >= trim_size:

            def read_and_ignore():
                input_stream.read_dictionary(
                    key_type_fn=key_type_fn,
                    value_type_fn=value_type_fn,
                    dictionary_length=dictionary_size,
                )
                return None

            return read_and_ignore
        return lambda: input_stream.read_dictionary(
            key_type_fn=key_type_fn,
            value_type_fn=value_type_fn,
            dictionary_length=dictionary_size,
        )
    if type_identifier in ["array", "variant"]:
        raise NotImplementedError(f"{type_identifier} type not implemented")

    raise NotImplementedError(f"{type_identifier} type not implemented")


def deserialize(
    input_stream: InputStream,
    schema_registry: dict,
    type_identifier: str,
    trim: bool,
    trim_size: int,
    is_enum: Optional[bool] = None,
):
    data_offset = input_stream.buffer.tell()
    if is_enum is None:
        is_enum = type_identifier in schema_registry["enums"]
    if is_enum:
        # TODO check how to deal with bitmask enums
        return read_enum(input_stream, type_identifier, schema_registry)
    else:
        # read the bitsream header
        input_stream.read_bitstream_header()
        res = OrderedDict()
        # read the fields in order
        schema = schema_registry["schemas"][type_identifier]
        for field in schema["fields"]:
            read_fn = get_read_fn(
                input_stream, schema_registry, field, trim=trim, trim_size=trim_size
            )
            field_name = field["name"]
            field_value = read_fn()
            # find size of field
            field_size = sys.getsizeof(field_value)
            if trim and field_size >= trim_size:
                field_value = None
            res[field_name] = field_value

        while input_stream.has_more_sections:
            group_id, group_size = input_stream.read_optional_group_header()
            # check if we have a group with this id
            if group_id not in schema["groups"]:
                input_stream.advance(group_size)
            else:
                # process it
                group_start_position = input_stream.buffer.tell()
                schema_group = schema["groups"][group_id]
                for field in schema_group["fields"]:
                    read_fn = get_read_fn(
                        input_stream,
                        schema_registry,
                        field,
                        trim=trim,
                        trim_size=trim_size,
                    )
                    field_name = field["name"]
                    field_value = read_fn()
                    field_size = sys.getsizeof(field_value)
                    if trim and field_size >= trim_size:
                        field_value = None
                    res[field_name] = field_value
                assert (
                    input_stream.buffer.tell() == group_start_position + group_size
                ), f"Warning: group {group_id} started at {group_start_position}, size is {group_size} but the current position is {input_stream.buffer.tell()}"
        data_end_offset = input_stream.buffer.tell()
        return res, data_offset, data_end_offset


def partition_by_identifier(schema_list: List[Dict]):
    return {
        f'{schema["object_namespace"]}::{schema["name"]}': schema
        for schema in schema_list
    }


def get_schema_registry(topic):
    schema_registry = topic["type_schema"]
    schema_registry = {
        k: partition_by_identifier(v) for k, v in schema_registry.items()
    }
    # the keys in enum schemas get stringified because it's over the wire via json
    # we may have to convert it back to the original type
    for enum_name, enum_schema in schema_registry["enums"].items():
        original_key_type = enum_schema["enum_class"]
        if original_key_type == "str":
            continue

        def get_transform_function(original_key_type: str) -> Callable[[str], any]:
            if original_key_type.startswith("int"):
                return int
            raise NotImplementedError()

        transform_function = get_transform_function(original_key_type)

        enum_schema["values"] = {
            transform_function(enum_key): enum_value
            for enum_key, enum_value in enum_schema["values"].items()
        }

    ## similarly we may have to rebuild the groups in the schema
    for schema_name, schema in schema_registry["schemas"].items():
        if "groups" not in schema:
            continue
        schema["groups"] = {v["identifier"]: v for v in schema["groups"].values()}
    return schema_registry


def extract_ark_message_from_bytes(topic, record_bytes):
    schema_registry = get_schema_registry(topic)

    input_stream = InputStream(record_bytes)
    ark_res, data_offset, data_end_offset = deserialize(
        input_stream,
        schema_registry,
        topic["type_name"],
        trim=False,
        trim_size=None,
    )
    return ark_res
