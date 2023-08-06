from __future__ import absolute_import
from .loadbalancer import LoadBalancer
from ..request_context import InternalRequestContext, \
    RpcInvoker, RpcServiceInfo, EndPoint
from ..ep.ep_request import EndPointRequest


class DirectLoadBalancer (LoadBalancer):

    '''
    显示指定了调用的目标地址的LoadBalancer实现方式
    '''

    def __init__(self):
        super().__init__()

    def check_alive(self):
        return True

    def chooseOne(self) -> EndPoint:
        return None

    def create_context(self, invoker: RpcInvoker, service: RpcServiceInfo) \
            -> InternalRequestContext:
        return InternalRequestContext(invoker, service, None)

    @property
    def type(self):
        return 'direct'

    def execute(self, req: EndPointRequest):
        ep = self._getEndPoint(req)
        result_data = req.execute(ep)
        return result_data

    def stream(self, req: EndPointRequest):
        ep = self._getEndPoint(req)
        result_stream = req.stream(ep)
        return result_stream

    def ws(self, req: EndPointRequest):
        ep = self._getEndPoint(req)
        conn = req.ws(ep)
        return conn

    def _getEndPoint(self, req: EndPointRequest):
        target_url = req.context.url
        port = int(target_url.port)
        if not port:
            port = 80 if target_url.protocol == 'http:' else 443
        return EndPoint(
            id="%s:%s" % (self.type, req.context.service.url),
            host=target_url.hostname,
            port=port
        )
