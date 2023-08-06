from __future__ import absolute_import

from abc import ABC, abstractmethod, abstractproperty
from ..request_context import AbstractInvoker, RpcServiceInfo, \
    RequestContext, EndPoint
from ..ep.ep_request import EndPointRequest


class LoadBalancer(ABC):
    @abstractmethod
    def create_context(self,
                       invoker: AbstractInvoker,
                       service: RpcServiceInfo) -> RequestContext:
        pass

    @abstractproperty
    def check_alive() -> bool:
        pass

    @abstractmethod
    def chooseOne(self) -> EndPoint:
        return None

    def request(self, method: str, req: EndPointRequest):
        if method == 'execute':
            return self.execute(req)
        elif method == 'stream':
            return self.stream(req)
        elif method == 'ws':
            return self.ws(req)
        raise RuntimeError('不支持的方法:' + method)

    @abstractmethod
    def execute(self, req: EndPointRequest):
        pass

    @abstractmethod
    def stream(self, req: EndPointRequest):
        pass

    @abstractmethod
    def ws(self, req: EndPointRequest):
        '''
        return WebSocket
        '''
        pass
