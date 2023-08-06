# Copyright (c) 2020 Thomas Kramer.
# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Implement packet transport over WebSockets.
"""

import logging
from typing import Any, Callable, Coroutine
from .packet import TLVPacket
from .base import Connection
import aiohttp.web

logger = logging.getLogger("WebSocketTransport")


class WebSocketConnection(Connection):
    """
    Abstraction over WebSocket connections.
    """

    def __init__(self, ws: aiohttp.web.WebSocketResponse):
        super().__init__()
        self.ws = ws

    async def read_packet(self) -> TLVPacket:
        data = await self.ws.receive_bytes()
        p = TLVPacket.from_buffer(data)
        return p

    async def write_packet(self, p: TLVPacket):
        await self.ws.send_bytes(p.encode())

    def close(self):
        self.ws.close()


async def run_websocket_server(
        handle_connection: Callable[[Connection], Coroutine],
        host: str,
        port: int):
    logger.info(f"Starting WebSocket server on {host}:{port}")

    async def websocket_handler(request):
        logger.debug('Websocket connection starting.')
        ws = aiohttp.web.WebSocketResponse()
        await ws.prepare(request)
        logger.debug('Websocket connection ready.')

        conn = WebSocketConnection(ws)
        await handle_connection(conn)
        return ws

    app = aiohttp.web.Application()
    app.router.add_route('GET', '/ws', websocket_handler)

    await aiohttp.web._run_app(app, host=host, port=port)
