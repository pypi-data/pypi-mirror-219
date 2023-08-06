import base64
import re
import struct
from collections import OrderedDict


DEBUG = False

# Primitive type handling for ROS builtin types
SIMPLE_TYPES_DICT = {  # see python module struct
    "int8": "b",
    "uint8": "B",
    # Python 2.6 adds in '?' for C99 _Bool, which appears equivalent to an uint8,
    # thus, we use uint8
    "bool": "B",
    "int16": "h",
    "uint16": "H",
    "int32": "i",
    "uint32": "I",
    "int64": "q",
    "uint64": "Q",
    "float32": "f",
    "float64": "d",
    # deprecated
    "char": "B",  # unsigned
    "byte": "b",  # signed
}

# endianess in struct format string
ENDIANNESS = {
    "little": "<",
    "big": ">",
}


class Deserializer:
    def deserialize(self, bytes, offset=0):
        raise NotImplementedError


class CustomROSDeserializer(Deserializer):
    # field regex, field type single word or package/class, optional array and array length in square brackets, single word field name
    # e.g. float64[9] covariance
    # this also ignores any constants defined in the message
    # e.g. float64 PI = 3.141592653589793
    field_regex = re.compile(r"^([\w/]+(\[\d*\])?)\s+(\w+)(\s*#.*)?$")
    array_regex = re.compile(r"^([\w/]+)\[(\d*)\]$")
    trim_cutoff = 1024

    def __init__(self, msg_definitions_dict={}, custom_deserializers={}, trim=False):
        self.msg_definitions_dict = {
            "time": {":is_simple": True, ":size": 8},
            "duration": {":is_simple": True, ":size": 8},
            "string": {
                ":is_simple": False,
                ":size": -1,
            },
            "Header": {
                ":is_simple": False,
                "seq": "uint32",
                "stamp": "time",
                "frame_id": "string",
                ":size": -1,
            },
        }
        self.msg_definitions_dict.update(msg_definitions_dict)
        self.trim = trim
        self.custom_deserializers = {
            "time": self.deserialize_time,
            "duration": self.deserialize_time,
            "string": self.deserialize_string,
            "Header": self.deserialize_header,
        }
        self.custom_deserializers.update(custom_deserializers or {})
        self.byte_order = ENDIANNESS["little"]

    def deserialize(self, message_type, bytes, offset=0):
        res = self.deserialize_message_generic(
            message_type,
            bytes,
            offset=offset,
            byte_order=self.byte_order,
        )[1]
        return res

    # CUSTOM DESERIALIZERS #
    def deserialize_string(
        self, field_type, bytes, offset=0, byte_order=ENDIANNESS["little"]
    ):
        # string is a uint32 length prefix followed by the string
        string_length = struct.unpack(
            f"{byte_order}{SIMPLE_TYPES_DICT['uint32']}", bytes[offset : offset + 4]
        )[0]
        offset += 4

        if self.trim and string_length > self.trim_cutoff:
            return offset + string_length, None

        field_value = bytes[offset : offset + string_length].decode("utf-8")
        return offset + string_length, field_value

    def deserialize_time(
        self, field_type, bytes, offset=0, byte_order=ENDIANNESS["little"]
    ):
        secs, nsecs = struct.unpack(
            f"{byte_order}2{SIMPLE_TYPES_DICT['uint32']}", bytes[offset : offset + 8]
        )
        offset += 8
        return offset, {"secs": secs, "nsecs": nsecs}

    def deserialize_array(
        self,
        field_type,
        bytes,
        package_name=None,
        offset=0,
        byte_order=ENDIANNESS["little"],
    ):
        match = self.array_regex.match(field_type)

        if not match:
            raise ValueError(f"Invalid field type: {field_type}")

        base_type, array_size = match.groups()
        if not array_size:
            # there's a uint32 length prefix to find out the array size
            array_size = struct.unpack(
                f"{byte_order}{SIMPLE_TYPES_DICT['uint32']}", bytes[offset : offset + 4]
            )[0]
            offset += 4
        array_size = int(array_size)

        if base_type in SIMPLE_TYPES_DICT:
            element_size = struct.calcsize(SIMPLE_TYPES_DICT[base_type])
            array_total_size = element_size * array_size

            if self.trim and array_total_size > self.trim_cutoff:
                return offset + array_total_size, None

            # can directly deserialize if it's a simple type
            if base_type == "char":
                field_value = bytes[offset : offset + array_total_size]
                return offset + array_size, base64.b64encode(field_value).decode(
                    "utf-8"
                )

            field_value = struct.unpack(
                f"{byte_order}{array_size}{SIMPLE_TYPES_DICT[base_type]}",
                bytes[offset : offset + array_total_size],
            )
            return offset + array_total_size, list(field_value)

        # otherwise, we need to deserialize each element individually
        field_value = []

        if self.trim and array_size > self.trim_cutoff:
            # save memory/cycles by not deserializing the array elements
            # if we can determine the size of the array elements
            if base_type not in self.msg_definitions_dict:
                base_type = f"{package_name}/{base_type}"
            if self.msg_definitions_dict[base_type][":is_simple"]:
                element_size = self.msg_definitions_dict[base_type][":size"]
                return offset + element_size * array_size, None

        for i in range(array_size):
            offset, element = self.deserialize_message_generic(
                base_type,
                bytes,
                package_name,
                offset,
            )
            field_value.append(element)

        if self.trim and len(field_value) > self.trim_cutoff:
            return offset, None

        return offset, field_value

    def deserialize_header(
        self, field_type, bytes, offset=0, byte_order=ENDIANNESS["little"]
    ):
        seq, stamp_secs, stamp_nsecs, frame_id_len = struct.unpack(
            f"{byte_order}4I", bytes[offset : offset + 16]
        )
        offset += 16
        frame_id = bytes[offset : offset + frame_id_len].decode("utf-8")
        offset += frame_id_len
        return offset, {
            "seq": seq,
            "stamp": {"secs": stamp_secs, "nsecs": stamp_nsecs},
            "frame_id": frame_id,
        }

    def deserialize_message_generic(
        self,
        message_type,
        bytes,
        current_package=None,
        offset=0,
        byte_order=ENDIANNESS["little"],
    ):
        message_type = message_type.split("/", 1)
        if len(message_type) == 1:
            # if message_type is not a fully qualified name, assume it's in the current package
            # there's an exception for the header message, which is in the std_msgs package
            # but we handle it separately
            if message_type[0] in ["string", "Header", "time"]:
                if message_type[0] == "Header":
                    fully_qualified_message_type = "std_msgs/Header"
                else:
                    fully_qualified_message_type = message_type[0]
            else:
                fully_qualified_message_type = current_package + "/" + message_type[0]
            package = current_package
        else:
            package = message_type[0]
            fully_qualified_message_type = package + "/" + message_type[1]

        if fully_qualified_message_type in self.custom_deserializers:
            # avoiding trimming here since we maybe want to allow custom trimming strategies
            return self.custom_deserializers[fully_qualified_message_type](
                field_type=fully_qualified_message_type, bytes=bytes, offset=offset
            )

        if fully_qualified_message_type not in self.msg_definitions_dict:
            raise Exception(f"Message type {fully_qualified_message_type} not found")
        msg_def_dict = self.msg_definitions_dict[fully_qualified_message_type]
        msg_dict = dict()

        for field_name, field_type in msg_def_dict.items():
            if field_name.startswith(":"):
                # internal helper field, skipping
                continue
            if field_type in self.custom_deserializers:
                offset, msg_dict[field_name] = self.custom_deserializers[field_type](
                    field_type=field_type, bytes=bytes, offset=offset
                )
            elif field_type in SIMPLE_TYPES_DICT:
                simple_element_size = struct.calcsize(SIMPLE_TYPES_DICT[field_type])
                msg_dict[field_name] = struct.unpack(
                    f"{byte_order}{SIMPLE_TYPES_DICT[field_type]}",
                    bytes[offset : offset + simple_element_size],
                )[0]
                offset += simple_element_size
            elif self.is_array(field_type):
                offset, msg_dict[field_name] = self.deserialize_array(
                    field_type,
                    bytes,
                    package,
                    offset,
                )
            else:
                offset, msg_dict[field_name] = self.deserialize_message_generic(
                    field_type,
                    bytes,
                    package,
                    offset,
                )
        return offset, msg_dict

    # UTILITY FUNCTIONS #

    def is_array(self, field_type):
        return self.array_regex.match(field_type) is not None

    def get_schema_registry_for_message_type(self, message_type):
        """
        Returns a dictionary of all the schema for message classes needed to serialize/deserialize the given message type.
        """
        if isinstance(message_type, dict):
            breakpoint()
        result = {message_type: list(self.msg_definitions_dict[message_type].items())}
        for field_name, field_type in self.msg_definitions_dict[message_type].items():
            if field_name.startswith(":"):
                # internal helper field, skipping
                continue

            if self.is_array(field_type):
                field_type = self.array_regex.match(field_type).group(1)

            if field_type in result or field_type in SIMPLE_TYPES_DICT:
                continue

            result[field_type] = list(self.msg_definitions_dict[field_type].items())
            dependent_res = self.get_schema_registry_for_message_type(field_type)
            result.update(dependent_res)
        return result

    def _extract_message_definition(self, message_type, message_def):
        """
        format of the further message defined in the message definition
        MSG: <message_name>
        keep parsing until we hit a line that starts with "==="
        """
        msg_name = message_type
        current_line = 0
        lines = message_def.splitlines()
        while current_line < len(lines):
            # fully qualified message name
            msg_name = msg_name
            self.msg_definitions_dict[msg_name] = OrderedDict()
            while current_line < len(lines):
                line = lines[current_line].strip()
                if not line or line.startswith("#"):
                    current_line += 1
                    continue
                if line.startswith("==="):
                    # skip comments
                    current_line += 1
                    while (
                        lines[current_line].strip().startswith("#")
                        or lines[current_line].strip() == ""
                    ):
                        current_line += 1
                    match_obj = re.search(r"^MSG: ([\w/]+)", lines[current_line])
                    if not match_obj:
                        print(
                            "No message name found", lines[current_line], current_line
                        )
                    else:
                        msg_name = match_obj.group(1)
                        current_line += 1
                    break

                match = self.field_regex.match(line)
                if not match:
                    # print(f"Skipping line {current_line}: {line}")
                    current_line += 1
                    continue
                # its still simpler to use split instead of regex groups
                words = line.split()
                field_type = words[0]
                field_name = words[1]

                self.msg_definitions_dict[msg_name][field_name] = field_type
                current_line += 1

    def extract_message_definition(self, message_type, message_def):
        message_delimiter = "================================================================================"
        messages = message_def.split(message_delimiter)
        msg_name_to_msg = OrderedDict()
        for message in messages[::-1][:-1]:
            message_lines = message.splitlines()
            for line in message_lines:
                if line.startswith("MSG:"):
                    msg_name_to_msg[line.split(" ")[1]] = message
        msg_name_to_msg[message_type] = messages[0]
        retry = []
        for msg_type, msg in msg_name_to_msg.items():
            if not self._extract_message_definition_with_size(msg_type, msg):
                retry.append(msg_type)
        for msg_type in retry:
            if not self._extract_message_definition_with_size(
                msg_type, msg_name_to_msg[msg_type]
            ):
                raise Exception(f"Failed to parse message {msg_type}")

    def _extract_message_definition_with_size(self, message_type, message_def):
        msg_name = message_type
        current_line = 0
        lines = message_def.splitlines()
        is_simple = True
        size = 0
        while current_line < len(lines):
            self.msg_definitions_dict[msg_name] = OrderedDict()
            while current_line < len(lines):
                line = lines[current_line].strip()
                if not line or line.startswith("#"):
                    current_line += 1
                    continue

                match = self.field_regex.match(line)
                if not match:
                    current_line += 1
                    continue
                # its still simpler to use split instead of regex groups
                words = line.split()
                field_type = words[0]
                field_name = words[1]
                # check if it's an array of known size
                array_regex = re.compile(r"(.*)\[(\d*)\]")
                match = array_regex.match(field_type)
                if match:
                    if match.groups()[1] != "":
                        # fixed length array
                        base_type = match.groups()[0]
                        if base_type == "string":
                            is_simple = False
                        elif (
                            base_type not in SIMPLE_TYPES_DICT
                            and not self.msg_definitions_dict[base_type][":is_simple"]
                        ):
                            is_simple = False
                        else:
                            if base_type in SIMPLE_TYPES_DICT:
                                size += int(match.groups()[1]) * struct.calcsize(
                                    SIMPLE_TYPES_DICT[base_type]
                                )
                            else:
                                size += (
                                    int(match.groups()[1])
                                    * self.msg_definitions_dict[base_type][":size"]
                                )
                    else:
                        # variable length array
                        is_simple = False
                else:
                    if field_type == "string":
                        is_simple = False
                    if field_type not in SIMPLE_TYPES_DICT:
                        if field_type in self.msg_definitions_dict:
                            if not self.msg_definitions_dict[field_type][":is_simple"]:
                                is_simple = False
                            else:
                                size += self.msg_definitions_dict[field_type][":size"]
                        else:
                            current_package = msg_name.split("/")[0]
                            field_type = current_package + "/" + field_type
                            if field_type not in self.msg_definitions_dict:
                                # clean up
                                del self.msg_definitions_dict[msg_name]
                                return False
                            if not self.msg_definitions_dict[field_type][":is_simple"]:
                                is_simple = False
                            else:
                                size += self.msg_definitions_dict[field_type][":size"]
                    else:
                        # simple types dict
                        size += struct.calcsize(SIMPLE_TYPES_DICT[field_type])

                self.msg_definitions_dict[msg_name][field_name] = field_type
                self.msg_definitions_dict[msg_name][":is_simple"] = is_simple

                self.msg_definitions_dict[msg_name][":size"] = (
                    -1 if not is_simple else size
                )
                current_line += 1
        return True


def make_dict(obj):
    from message_converter import convert_ros_message_to_dictionary

    return convert_ros_message_to_dictionary(obj)


def get_message_class(message_type):
    import importlib
    import sys

    import roslib

    message_class = roslib.message.get_message_class(message_type)
    if message_class is None:
        package, name = message_type.split("/")
        try:
            if f"{package}.msg._{name}" in sys.modules:
                importlib.reload(sys.modules[f"{package}.msg"])
            message_module = importlib.import_module(f"{package}.msg._{name}")
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                f"Failed importing class for message_type {message_type}."
            )
        message_class = getattr(message_module, name)
    return message_class
