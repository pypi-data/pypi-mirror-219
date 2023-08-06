# Asgiproxify - An ASGI middleware for dynamic reverse proxy
# Copyright (C) 2023 William Goodspeed (龚志乐)
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this library.  If not, see <https://www.gnu.org/licenses/>.

"""An ASGI middleware for dynamic reverse proxy."""

import asyncio
import aiohttp


class AsgiproxifyHandler():
    """Handle the proxy request from the AsgiProxify middleware."""

    def __init__(self, scope):
        self.scope = scope

    def make_request_url(self):
        """Specify which URL will be requested from aiohttp client."""
        return 'http://example.org/'

    def make_request_cookies(self):
        """Specify which cookies will be used from aiohttp client."""
        return {}

    def make_request_headers(self):
        """Specify which headers will be used from aiohttp client."""
        req_headers = {k.decode(): v.decode()
                       for k, v in self.scope['headers']}
        req_headers.pop('host', None)
        return req_headers

    def make_response_headers(self, upstream_headers):
        """Specify which headers will be returned to the actual client."""
        headers = dict(upstream_headers)
        headers.pop('Server', None)
        headers.pop('Date', None)

        resp_headers = list(headers.items())
        return resp_headers

    def make_request(self, session):
        """Generate a aiohttp request for streaming contents."""
        return session.request('GET',  self.make_request_url(),
                               cookies=self.make_request_cookies(),
                               headers=self.make_request_headers(),)


class Asgiproxify():
    """An ASGI middleware for dynamic reverse proxy."""
    app = None
    reg = {}

    def __init__(self, app=None):
        """Initialize an Asgiproxify app with optional fallback app."""
        self.to(app)

    def to(self, app):
        """Set the ASGI app which will be forwarded to if no proxy."""
        self.app = app

    def install(self, leading_path, handler):
        """Install a proxy handler for handling `leading_path'."""
        self.reg[leading_path] = handler

    def register(self, leading_path):
        """Register the current class as a porxy handler for `leading_path'."""
        def decorator(c):
            self.install(leading_path, c)
        return decorator

    async def _handle_proxy(self, scope, receive, send, handler):
        handler_i = handler(scope)
        await receive()

        async def reverse_proxy_task():
            async with aiohttp.ClientSession(auto_decompress=False) as session:
                async with handler_i.make_request(session) as resp:
                    await send({
                        'type': 'http.response.start',
                        'status': resp.status,
                        'headers': handler_i
                        .make_response_headers(resp.headers),
                    })
                    async for chunk, _ in resp.content.iter_chunks():
                        await send({
                            'type': 'http.response.body',
                            'body': chunk,
                            'more_body': True,
                        })
                    await send({'type': 'http.response.body'})

        task = asyncio.create_task(reverse_proxy_task())
        while True:
            ev = await receive()
            if ev['type'] == 'http.disconnect':
                task.cancel()
                return

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)

        handler = None

        for leading_path, proxy_handler in self.reg.items():
            if scope['path'].startswith(leading_path):
                handler = proxy_handler

        if not handler:
            return await self.app(scope, receive, send)
        return await self._handle_proxy(scope, receive, send, handler)
