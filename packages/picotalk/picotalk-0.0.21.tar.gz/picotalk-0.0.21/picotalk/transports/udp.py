# Copyright (c) 2020 Thomas Kramer.
# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Implement packet transport over UDP.
"""

import asyncio
import logging
import struct
from typing import Any, Callable, Coroutine, Dict, Optional
import nacl.utils
from .packet import TLVPacket
from .base import Connection

logger = logging.getLogger("UdpTransport")


class UdpPacketRouter:
    """
    Routes incoming UDP packets based on their 'stream ID' tag.
    """

    _stream_id_struct = struct.Struct(">L")

    def __init__(self):
        self.streams: Dict[int, Callable[[bytes, Any], None]] = dict()
        self.transport: Optional[asyncio.DatagramTransport] = None

    def register_stream(self, stream_id: int, callback: Callable[[bytes, Any], None]):
        """
        :param stream_id:
        :param callback: Function that will be called when a packet with this stream ID arrives.
            This should take two arguments: The payload data (bytes) and the source address (Tuple[str, int]).
        """
        logger.debug(f"Register stream ID: {stream_id}")
        if stream_id in self.streams:
            raise Exception(f"Stream with ID {stream_id} already exists.")

        self.streams[stream_id] = callback

    def remove_stream(self, stream_id: int):
        logger.debug(f"Remove stream ID: {stream_id}")
        if stream_id in self.streams:
            del self.streams[stream_id]

    def send_datagram(self, stream_id: int, data: bytes, dest_addr):
        if self.transport is not None:

            stream_id_tag = UdpPacketRouter._stream_id_struct.pack(stream_id)
            data = stream_id_tag + data
            self.transport.sendto(data, dest_addr)
        else:
            logger.error("Transport is not set!")

    def route_datagram(self, data: bytes, source_addr):
        # logger.debug(f"Routing UDP packet from {source_addr}")
        tag_len = UdpPacketRouter._stream_id_struct.size
        if len(data) < tag_len:
            logger.debug("Dropping packet: too short")
        else:
            # Decode the stream ID.
            stream_id, = UdpPacketRouter._stream_id_struct.unpack_from(data)

            callback = self.streams.get(stream_id)
            if callback is None:
                logger.debug(f"Stream not registered: {stream_id}")
            else:
                callback(data[tag_len:], source_addr)

    @staticmethod
    def random_stream_id() -> int:
        """
        Generate a fresh stream ID for routing the UDP packets.
        """
        random_bytes = nacl.utils.random(UdpPacketRouter._stream_id_struct.size)
        udp_stream_id, = UdpPacketRouter._stream_id_struct.unpack(random_bytes)
        return udp_stream_id


class UdpConnection(Connection):

    def __init__(self, router: UdpPacketRouter, stream_id: int, dest_addr):
        super().__init__()
        assert not self.is_closed()
        self.router = router
        self.stream_id = stream_id
        # Address of other endpoint.
        self.dest_addr = dest_addr
        # Receive timeout in seconds.
        self.receive_timeout = 120

        self.input_queue = asyncio.Queue(maxsize=4)

        def receive_callback(data: bytes, addr):
            if self.dest_addr is None:
                # Remember peer address when first seen.
                self.dest_addr = addr

            if addr == self.dest_addr:
                # Accept only packets coming from the expected address.
                if not self.input_queue.full():
                    self.input_queue.put_nowait(data)
                else:
                    logger.debug("UDP input queue is full. Dropping packet.")
            else:
                logger.debug("Address mismatch: {} != {}".format(addr, dest_addr))

        router.register_stream(stream_id, receive_callback)

    async def read_packet(self, timeout=None) -> TLVPacket:
        """
        :param timeout: Maximal waiting time for the packet.
            `timeout=0` disables the timeout.
        """

        if self.is_closed():
            raise ConnectionError("Connection is already closed.")

        if timeout is None:
            timeout = self.receive_timeout

        try:
            if timeout > 0:
                data = await asyncio.wait_for(self.input_queue.get(), timeout=timeout)
            else:
                data = await self.input_queue.get()

            return TLVPacket.from_buffer(data)
        except asyncio.TimeoutError as e:
            # Close the connection.
            logger.debug("Timeout: close connection.")
            self.router.remove_stream(self.stream_id)
            raise ConnectionError("Connection closed by timeout.")

    async def write_packet(self, p: TLVPacket):
        assert self.dest_addr is not None, "Destination address is not yet known."
        self.router.send_datagram(self.stream_id, p.encode(), self.dest_addr)

    def close(self):
        super().close()
        self.router.remove_stream(self.stream_id)


class UdpProtocol(asyncio.DatagramProtocol):

    def __init__(self, router: UdpPacketRouter):
        super().__init__()
        self.router = router
        self.transport: asyncio.DatagramTransport = None

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport
        self.router.transport = transport

    def datagram_received(self, data, addr):
        # logger.debug(f"Received UDP packet from {addr}")
        self.router.route_datagram(data, addr)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        # TODO: Notify router!
        logger.warning("UDP connection lost: {}".format(exc))


async def run_udp_server(
        handle_connection: Callable[[Connection], Coroutine],
        server_addr: str,
        server_udp_port: int) -> UdpPacketRouter:
    logger.info(f"Starting UDP server on {server_addr}:{server_udp_port}")

    loop = asyncio.get_running_loop()

    router = UdpPacketRouter()

    # One protocol instance will be created to serve all
    # client requests.
    udp_transport, protocol = await loop.create_datagram_endpoint(
        lambda: UdpProtocol(router),
        local_addr=(server_addr, server_udp_port)
    )
    logger.info(f"UDP server listening on {server_addr}:{server_udp_port}")

    # # TODO: close the transport if server is shut down.
    # transport.close()

    return router


async def open_udp_connection(server_addr: str, port: int, stream_id: int) -> UdpConnection:
    """
    Open UDP client connection.
    """

    # Open UDP connection.
    loop = asyncio.get_running_loop()
    udp_remote_addr = (server_addr, port)

    router = UdpPacketRouter()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UdpProtocol(
            router
        ),
        remote_addr=udp_remote_addr)

    addr, port = transport._address

    logger.debug("UDP connection to {}:{}".format(addr, port))

    conn = UdpConnection(router, stream_id=stream_id, dest_addr=(addr, port))

    return conn
