import struct
import io

# The magic bits to indicate the byte is a header.
BITSTREAM_HEADER_MAGIC = 0xD0

# THe magic bits to indicate the byte is a group.
BITSTREAM_GROUP_MAGIC = 0xE0

# Indicates that this header/group has at least one following section
# that needs to be read.
BITSTREAM_HAS_FOLLOWING_SECTION = 0x04


class InputStream:
    """
    This class allows you to read serialized rbuf structures into native
    Python structures. It closely mimics the C++ API.
    """

    #
    # This block of structures is a pre-initialized/static set of structures meant
    # to improve performance of decoding individual primitives.
    #

    _decoder_uint8 = struct.Struct("<B")
    _decoder_uint16 = struct.Struct("<H")
    _decoder_uint32 = struct.Struct("<L")
    _decoder_uint64 = struct.Struct("<Q")
    _decoder_int8 = struct.Struct("<b")
    _decoder_int16 = struct.Struct("<h")
    _decoder_int32 = struct.Struct("<l")
    _decoder_int64 = struct.Struct("<q")
    _decoder_float = struct.Struct("<f")
    _decoder_double = struct.Struct("<d")
    _decoder_group = struct.Struct("<BBL")

    def __init__(self, buffer):
        """
        Initializes the stream against the given buffer of bytes.
        """

        self.buffer = io.BytesIO(buffer)
        self.has_more_sections = False

    def read_bitstream_header(self):
        """
        Reads the bitstream header from the stream. These headers
        denote the start of a new serialized structure, and help
        indicate version information or if different sections are
        present.
        """
        # print(f"/read_bitstream_header: {self.buffer.tell()}")
        header = self.read_uint8()

        # Ensure the header magic bits are set.
        if (header & 0xF0) != BITSTREAM_HEADER_MAGIC:
            raise Exception(
                "Tried to read a bitstream header, but the header had the incorrect magic numbers. "
                "This indicates the stream is corrupt, or is not a rbuf stream."
            )

        # We can only decode version one with this code.
        if (header & 0x03) != 0x01:
            raise Exception(
                "Tried to read a bitstream header, but it had an unexpected version number. This "
                "software only supports version 1."
            )

        # Store off if we have more sections...
        self.has_more_sections = (header & BITSTREAM_HAS_FOLLOWING_SECTION) > 0

        # If the last bit is set, then we have some kind of unexpected
        # bitstream error.
        if (header & 0x08) != 0x00:
            raise Exception(
                "Tried to read a bitstream header, but this header indicates the stream has groups, "
                "which this software does not support."
            )

    def read_optional_group_header(self):
        """
        Reads a group header from the bitstream, updating if we have additional sections or not,
        and returning a tuple containing the parsed identifier and group size. Throws if the next
        byte does not appear to be a group header.
        """
        # print(f"read_optional_group_header: {self.buffer.tell()}")
        header = InputStream._decoder_group.unpack(self.buffer.read(6))

        # Throw if this isn't a group
        if (header[0] & 0xF0) != BITSTREAM_GROUP_MAGIC:
            raise Exception(
                "Tried to read a bitstream group header, but the header had an incorrect magic "
                "number. This indicates the stream is corrupt, or is not an rbuf stream."
            )

        # Record if we have additional sections
        self.has_more_sections = (header[0] & BITSTREAM_HAS_FOLLOWING_SECTION) > 0

        # Throw if we have any other fields set, something is wrong and we're an incorrect
        # version or were wrong that it was a group.
        if (header[0] & 0x0B) != 0x00:
            raise Exception(
                "Tried to read a bitstream group header, but the header had additional flags specified that were unknown."
            )

        # Return the group identifier and size as a tuple
        return header[1:]

    def advance(self, length):
        """
        Advances the bitstream by length bytes, throwing if this would go outside of the bounds
        of the buffer. This can be used to 'read' data from the stream (skip it).
        """

        self.buffer.seek(length, 1)

    def read_string(self):
        """
        Reads the next string from the input stream, throwing if there is
        a bitstream error.
        """

        # Read the string length first, it's a 32-bit integer.
        string_length = self.read_uint32()

        # The next string_length bytes are returned as the actual string data...
        string = self.buffer.read(string_length)

        return string.decode("utf-8")

    def read_object(self, object_class):
        """
        Reads the next object from the input stream. The object class is used to instantiate
        the object.
        """

        # Push state before deserializing
        pushed_flags = self.has_more_sections
        self.has_more_sections = False

        # Create the object and deserialize
        output = object_class()
        output.deserialize(self)

        # Restore state and return the final result
        self.has_more_sections = pushed_flags
        return output

    def read_variant(self, types):
        """
        Reads a variant from the given list of possibilities.
        """

        index = self.read_uint8()
        length = self.read_uint32()

        # If the index isn't in our types, skip it, and return the first type
        # to match C++ logic
        if index not in types:
            self.advance(length)

            entries = list(types.values())
            return entries[0]()

        # Now we can read the object given the passed-in type.
        return self.read_object(types[index])

    def read_array_size(self, fixed_array_size):
        """
        Reads the array size and returns it. If fixed_array_size is not none, just
        returns that value.
        """

        if fixed_array_size is None:
            return self.read_uint32()
        else:
            return fixed_array_size

    def read_object_array(self, object_class, fixed_array_size=None):
        """
        Reads an array containing the given object class.

        If fixed_array_size is specified, assumes the array size is fixed, and uses that
        number instead of reading the length from the bitsteam.
        """

        # Get the desired array length...
        array_length = self.read_array_size(fixed_array_size)

        # Create the array and read objects into it.
        output = []

        while array_length > 0:
            output.append(self.read_object(object_class))
            array_length -= 1

        return output

    def read_array(self, read_fn, fixed_array_size=None):
        """
        Reads an array with the given function lambda.

        If fixed_array_size is specified, assumes the array size is fixed, and uses that
        number instead of reading the length from the bitsteam.
        """

        # Get the desired array length...
        array_length = self.read_array_size(fixed_array_size)

        # Create the array and read objects into it.
        output = []

        while array_length > 0:
            output.append(read_fn())
            array_length -= 1

        return output

    def read_primitive_array(self, format_string, item_length, fixed_array_size=None):
        """
        Reads a primitive array of the given format, checking to make sure we have
        enough bytes left in the bitstream to satisfy the request.

        If fixed_array_size is specified, assumes the array size is fixed, and uses that
        number instead of reading the length from the bitsteam.
        """

        # Read the length of the array and check to make sure we have enough room
        # for the content.
        array_length = self.read_array_size(fixed_array_size)
        byte_size = array_length * item_length

        # Now read the actual array
        read_data = struct.unpack(
            "<" + str(array_length) + format_string, self.buffer.read(byte_size)
        )

        return list(read_data)

    def read_byte_buffer(self):
        """
        Reads a 'byte buffer' (in Python, this is just an array of uint8 objects).
        """

        # Read the length in first...
        array_length = self.read_uint32()

        # Now just read the raw bytes. No need to do any packing/unpacking/etc, this is just
        # an arary of bytes.
        return self.buffer.read(array_length)

    def read_guid(self):
        """
        Reads a GUID from the bitstream, which is essentially a 16-byte array that we
        return into a string for Python consumption.
        """

        # Read the raw 16 bytes in.
        raw_bytes = self.buffer.read(16)

        # Convert the array into a hex guid, the hard way. Note that in Ark
        # the first 8 bytes are behind the second 8 bytes, and 'backwards', as
        # it tries to match little endian notation for two 8 byte integers for
        # some reason. We should move this into a class.
        output = ""

        index = 7
        while index >= 0:
            if index == 1 or index == 3:
                output += "-"

            output += "{:02x}".format(raw_bytes[index])
            index -= 1

        index = 15
        while index >= 8:
            if index == 15 or index == 13:
                output += "-"

            output += "{:02x}".format(raw_bytes[index])
            index -= 1

        return output

    def read_dictionary(self, key_type_fn, value_type_fn, dictionary_length=None):
        """
        Reads in a dictioanry. The key and value function actually read data from
        the underlying bitstream and place the contents into said dictionary.
        """

        dictionary_length = self.read_array_size(dictionary_length)
        result = {}
        # print(f"dictionary_length: {dictionary_length}")

        while dictionary_length > 0:
            key = key_type_fn()
            value = value_type_fn()

            result[key] = value
            dictionary_length -= 1

        return result

    def read_optional(self, read_fn):
        """
        Reads in an optional. If set, uses the read function to read the primitive,
        otherwise, returns None.
        """

        if self.read_bool():
            return read_fn()
        else:
            return None

    def read_bool(self):
        return self.read_uint8() > 0

    def read_uint8(self):
        return InputStream._decoder_uint8.unpack(self.buffer.read(1))[0]

    def read_uint16(self):
        return InputStream._decoder_uint16.unpack(self.buffer.read(2))[0]

    def read_uint32(self):
        return InputStream._decoder_uint32.unpack(self.buffer.read(4))[0]

    def read_uint64(self):
        return InputStream._decoder_uint64.unpack(self.buffer.read(8))[0]

    def read_int8(self):
        return InputStream._decoder_int8.unpack(self.buffer.read(1))[0]

    def read_int16(self):
        return InputStream._decoder_int16.unpack(self.buffer.read(2))[0]

    def read_int32(self):
        return InputStream._decoder_int32.unpack(self.buffer.read(4))[0]

    def read_int64(self):
        return InputStream._decoder_int64.unpack(self.buffer.read(8))[0]

    def read_float(self):
        return InputStream._decoder_float.unpack(self.buffer.read(4))[0]

    def read_double(self):
        return InputStream._decoder_double.unpack(self.buffer.read(8))[0]
