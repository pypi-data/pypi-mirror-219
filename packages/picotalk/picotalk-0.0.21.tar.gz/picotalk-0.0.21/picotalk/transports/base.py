# Copyright (c) 2020 Thomas Kramer.
# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Abstraction layer for network connections.

Network connections are abstracted as (not necessarily reliable) packet based connections.
"""

import logging
from .packet import TLVPacket

logger = logging.getLogger('PacketTransport')


class Connection:
    """
    Base class of connection instances.
    """

    def __init__(self):
        self._is_closed = False
        self._extra_info = dict()

    async def read_packet(self) -> TLVPacket:
        raise NotImplementedError

    async def write_packet(self, data: TLVPacket):
        raise NotImplementedError

    def is_closed(self) -> bool:
        return self._is_closed

    def close(self):
        self._is_closed = True

    def get_extra_info(self, key):
        """
        Get user-defined data of this connection.
        :param key: Key of the entry.
        """
        return self._extra_info.get(key)

    def set_extra_info(self, key, value):
        """
        Associate user-defined data with this connection.
        :param key: Key.
        :param value: Value of the data.
        """
        self._extra_info[key] = value
