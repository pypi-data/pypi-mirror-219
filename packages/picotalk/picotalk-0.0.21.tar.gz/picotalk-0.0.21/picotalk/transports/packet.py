# Copyright (c) 2020 Thomas Kramer.
# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Data structure of the basic message packet that is sent between server and clients.
Includes also serialization and deserialization.
"""

from enum import Enum
import struct
from typing import Dict, Tuple
import asyncio
import json


class PacketType(Enum):
    AudioFrame = 1
    JSON = 2
    Binary = 3


class TLVPacket:
    """
    Type-length-value packet for transmission of different data types over the network.
    """

    # Tag format for `struct.pack`.
    # Type: 1 byte, length: 2 bytes unsigned integer
    # Big endian.
    _tag_struct = struct.Struct('>BHHH')

    def __init__(self, _type: PacketType, data: bytes,
                 src_addr: int = 0, dest_addr: int = 0):
        assert isinstance(data, bytes), f"{type(data)}"
        assert isinstance(_type, PacketType)
        self.type: PacketType = _type
        self.src_addr: int = src_addr
        self.dest_addr: int = dest_addr
        self.data: bytes = data

    @staticmethod
    def from_dict(**kwargs):
        data = bytes(json.dumps(kwargs), 'utf-8')
        return TLVPacket(PacketType.JSON, data)

    def to_dict(self) -> Dict:
        """
        Parse the JSON content into a dict.

        Raises an error if this is not a JSON packet or the JSON is not well formatted.
        """
        assert self.type == PacketType.JSON

        return json.loads(self.data)

    def encode(self) -> bytes:
        """
        Encode the packet into bytes.
        """
        # Type: 1 byte
        # Length: uint16
        # Data: n bytes
        tag = TLVPacket._tag_struct.pack(
                          self.type.value, len(self.data),
                          self.src_addr, self.dest_addr
                          )
        return tag + self.data

    @staticmethod
    def decode_tag(tag_data: bytes) -> Tuple[PacketType, int, int, int]:
        """
        Raises a `ValueError` if the type field is invalid.
        """
        assert len(tag_data) >= TLVPacket._tag_struct.size
        type_num, length, src_addr, dest_addr = TLVPacket._tag_struct.unpack(tag_data)

        type = PacketType(type_num)

        return type, length, src_addr, dest_addr

    @staticmethod
    async def read_async(reader: asyncio.StreamReader):
        """
        Read packet from a asyncio.StreamReader
        """
        tag_data = await reader.readexactly(TLVPacket._tag_struct.size)
        type, length, src_addr, dest_addr = TLVPacket.decode_tag(tag_data)
        data = await reader.readexactly(length)

        return TLVPacket(type, data, src_addr=src_addr, dest_addr=dest_addr)

    @staticmethod
    def from_buffer(buffer: bytes):
        """
        Read packet from a `bytes` object.
        """
        assert isinstance(buffer, bytes), f"{type(buffer)}"
        l = TLVPacket._tag_struct.size
        type, length, src_addr, dest_addr = TLVPacket.decode_tag(buffer[:l])
        assert len(buffer) == l + length, "Buffer size does not match."

        return TLVPacket(type, buffer[l:l + length], src_addr=src_addr, dest_addr=dest_addr)
