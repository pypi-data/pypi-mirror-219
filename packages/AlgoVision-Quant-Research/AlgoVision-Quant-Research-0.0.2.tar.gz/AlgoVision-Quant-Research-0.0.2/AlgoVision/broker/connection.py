# Classes for handling connections to the
import logging
import time
import asyncio
from asyncio import Queue, CancelledError
from contextlib import asynccontextmanager, suppress
from typing import List, Union, AsyncIterable
from decimal import Decimal
import atexit
from dataclasses import dataclass

from aiohttp.client_reqrep import ClientResponse
import requests
import websockets
import aiohttp
from aiohttp.typedefs import StrOrURL
# from yapic import json as json_parser

LOG = logging.getLogger('feedhandler')

class Connection:
    raw_data_callback = None

    async def read(self) -> bytes:
        raise NotImplementedError

    async def write(self, msg: str):
        raise NotImplementedError


class AsyncConnection(Connection):
    conn_count: int =0
    def __init__(self, conn_id: str, authentication=None, subscription=None):
        """
        conn_id: str
            the unique identifier for the connection
        authentication: Callable
            function pointer that will be invoked directly before the connection
            is attempted. Some connections may need to do authentication at this point.
        subscription: dict
            optional connection information
        """
        AsyncConnection.conn_count += 1
        self.id: str = conn_id
        self.received: int = 0
        self.sent: int = 0
        self.last_message = None
        self.authentication = authentication
        self.subscription = subscription
        self.conn: Union[websockets.WebSocketClientProtocol, aiohttp.ClientSession] = None
        atexit.register(self.__del__)

    def __del__(self):
        # best effort clean up. Shutdown should be called on Feed/Exchange classes
        # and any user of the Async connection should use a context manager (via connect)
        # or call close manually. If not, we *might* be able to clean up the connection on exit
        try:
            if self.is_open:
                asyncio.ensure_future(self.close())
        except (RuntimeError, RuntimeWarning):
            # no event loop, ignore error
            pass

    @property
    def uuid(self):
        return self.id

    @asynccontextmanager
    async def connect(self):
        await self._open()
        try:
            yield self
        finally:
            await self.close()

    async def _open(self):
        raise NotImplementedError

    @property
    def is_open(self) -> bool:
        raise NotImplementedError

    async def close(self):
        if self.is_open:
            conn = self.conn
            self.conn = None
            await conn.close()
            LOG.info('%s: closed connection %r', self.id, conn.__class__.__name__)
class WSAsyncConn(AsyncConnection):

    def __init__(self, address: str, conn_id: str, authentication=None, subscription=None, **kwargs):
        """
        address: str
            the websocket address to connect to
        conn_id: str
            the identifier of this connection
        kwargs:
            passed into the websocket connection.
        """
        if not address.startswith("wss://"):
            raise ValueError(f'Invalid address, must be a wss address. Provided address is: {address!r}')
        self.address = address
        super().__init__(f'{conn_id}.ws.{self.conn_count}', authentication=authentication, subscription=subscription)
        self.ws_kwargs = kwargs

    @property
    def is_open(self) -> bool:
        return self.conn and not self.conn.closed

    async def _open(self):
        if self.is_open:
            LOG.warning('%s: websocket already open', self.id)
        else:
            LOG.debug('%s: connecting to %s', self.id, self.address)
            if self.raw_data_callback:
                await self.raw_data_callback(None, time.time(), self.id, connect=self.address)
            if self.authentication:
                self.address, self.ws_kwargs = await self.authentication(self.address, self.ws_kwargs)

            self.conn = await websockets.connect(self.address, **self.ws_kwargs)
        self.sent = 0
        self.received = 0
        self.last_message = None

    async def read(self) -> AsyncIterable:
        if not self.is_open:
            LOG.error('%s: connection closed in read()', id(self))
            # raise ConnectionClosed
            pass
        if self.raw_data_callback:
            async for data in self.conn:
                self.received += 1
                self.last_message = time.time()
                await self.raw_data_callback(data, self.last_message, self.id)
                yield data
        else:
            async for data in self.conn:
                self.received += 1
                self.last_message = time.time()
                yield data

    async def write(self, data: str):
        if not self.is_open:
#             raise ConnectionClosed
            pass

        if self.raw_data_callback:
            await self.raw_data_callback(data, time.time(), self.id, send=self.address)
        await self.conn.send(data)
        self.sent += 1


@dataclass
class WebsocketEndpoint:
    address: str
    sandbox: str = None
    instrument_filter: str = None
    channel_filter: str = None
    limit: int = None
    options: dict = None
    authentication: bool = None

    def __post_init__(self):
        defaults = {'ping_interval': 10, 'ping_timeout': None, 'max_size': 2**23, 'max_queue': None, 'read_limit': 2**18}
        if self.options:
            defaults.update(self.options)
        self.options = defaults

    def subscription_filter(self, sub: dict) -> dict:
        if not self.instrument_filter and not self.channel_filter:
            return sub
        ret = {}
        for chan, syms in sub.items():
            if self.channel_filter and chan not in self.channel_filter:
                continue
            ret[chan] = []
            if not self.instrument_filter:
                ret[chan].extend(sub[chan])
            else:
                if self.instrument_filter[0] == 'TYPE':
                    # ret[chan].extend([s for s in syms if str_to_symbol(s).type in self.instrument_filter[1]])
                    ret[chan].extend([s for s in syms if s.type in self.instrument_filter[1]])
                elif self.instrument_filter[0] == 'QUOTE':
                    # ret[chan].extend([s for s in syms if str_to_symbol(s).quote in self.instrument_filter[1]])
                    ret[chan].extend([s for s in syms if s.quote in self.instrument_filter[1]])

                else:
                    raise ValueError('Invalid instrument filter type specified')
        return ret

    def get_address(self, sandbox=False):
        if sandbox and self.sandbox:
            return self.sandbox
        return self.address


@dataclass
class Routes:
    instruments: Union[str, list]
    currencies: str = None
    funding: str = None
    open_interest: str = None
    liquidations: str = None
    stats: str = None
    authentication: str = None
    l2book: str = None
    l3book: str = None


@dataclass
class RestEndpoint:
    address: str
    sandbox: str = None
    instrument_filter: str = None
    routes: Routes = None

    def route(self, ep, sandbox=False):
        endpoint = self.routes.__getattribute__(ep)
        api = self.sandbox if sandbox and self.sandbox else self.address
        return api + endpoint if isinstance(endpoint, str) else [api + e for e in endpoint]