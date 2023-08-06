import re
from starlette.datastructures import Headers
from starlette.types import Receive, Scope, Send
from .. import header_filter as filter

pattern = re.compile('-([a-z])', re.IGNORECASE)


class ServiceContextMiddleware:
    def __init__(self, app, converters):
        self._app = app
        self._converters = converters

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        headers = Headers(scope=scope)
        headerNames = headers.keys()
        processors = filter.process(headerNames)
        tracingHeaders = processors['tracingHeaders']
        extrasHeaders = processors['extrasHeaders']

        tracing = {}
        for header_name in tracingHeaders:
            tracing[header_name] = headers[header_name]
        scope['tracing'] = tracing

        extras = {}
        for header_name in extrasHeaders:
            self._resolve_extras_value(extras, headers, header_name)

        scope['extras'] = extras
        await self._app(scope, receive, send)

    def _resolve_extras_value(self, extras: dict, headers: Headers, name: str):
        key = pattern.sub(to_upper, name.replace('x-', ''))
        converter = self._converters.get(name)
        value = headers[name]
        if converter:
            value = converter(value)
        extras[key] = value


def to_upper(matched):
    text = matched.group(1)
    return text.upper()
