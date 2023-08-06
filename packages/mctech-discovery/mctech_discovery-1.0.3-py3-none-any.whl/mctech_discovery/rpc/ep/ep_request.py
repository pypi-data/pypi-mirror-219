from __future__ import absolute_import
from typing import Any
from abc import ABC, abstractmethod
from ..request_context import RequestContext, EndPoint


class EndPointRequest(ABC):
    def __init__(self, context: RequestContext):
        self.context = context

    @abstractmethod
    def execute(self, ep: EndPoint) -> Any:
        pass

    @abstractmethod
    def stream(self, ep: EndPoint):
        '''
        :return Stream
        '''
        pass

    @abstractmethod
    def ws(self, ep: EndPoint):
        '''
        :return Stream
        '''
        from websocket import WebSocket
        return WebSocket()
