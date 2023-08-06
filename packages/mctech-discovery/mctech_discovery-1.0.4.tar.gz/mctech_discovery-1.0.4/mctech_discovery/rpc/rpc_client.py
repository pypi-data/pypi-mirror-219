from __future__ import absolute_import
from .ep.simple_ep_request import SimpleEndPointRequest
from .request_context import WebSocketInvoker, RpcInvoker, PipeRpcInvoker, \
    AbstractInvoker, RpcServiceInfo
from ..rpc import lb as lb_factory


def request_creator(context): return SimpleEndPointRequest(context)


methods = set(['get', 'post', 'put', 'delete', 'patch'])
_request_creator = request_creator


class RpcClient():
    def __init__(self, service: RpcServiceInfo = None):
        self.service = service

    def get(self, invoker: RpcInvoker, service: RpcServiceInfo = None):
        return _verb_func('get', self, invoker, service)

    def post(self, invoker: RpcInvoker, service: RpcServiceInfo = None):
        return _verb_func('post', self, invoker, service)

    def put(self, invoker: RpcInvoker, service: RpcServiceInfo = None):
        return _verb_func('put', self, invoker, service)

    def patch(self, invoker: RpcInvoker, service: RpcServiceInfo = None):
        return _verb_func('patch', self, invoker, service)

    def delete(self, invoker: RpcInvoker, service: RpcServiceInfo = None):
        return _verb_func('delete', self, invoker, service)

    def ws(self, invoker: WebSocketInvoker, service: RpcServiceInfo = None):
        if self.service and service:
            raise RuntimeError('已绑定serivce，不允许再传入新的service')

        if self.service:
            # 当前rpc对象已绑定service
            return rpc.ws(invoker, self.service)

        return _do_request(invoker, service, 'ws')

    def stream(self, invoker: PipeRpcInvoker, service: RpcServiceInfo = None):
        if self.service and service:
            raise RuntimeError('已绑定serivce，不允许再传入新的service')

        if self.service:
            # 当前rpc对象已绑定service
            return rpc.stream(invoker, self.service)

        method = invoker.method
        assert method, '使用stream方法，invoker.method不能为空'

        method = method.lower()
        assert methods.__contains__(method), '不支持的方法:' + method
        return _do_request(invoker, service, 'stream')

    def bind(self, service: RpcServiceInfo):
        '''
        需要调用的服务的信息
        '''
        return RpcClient(service)

    def set_creator(self, creator):
        '''
        :param creator
        :type 'creator' context => EndPointRequest
        '''
        if not creator:
            raise RuntimeError('creator不能为空值')

        _request_creator = creator  # noqa F841


def _verb_func(method: str, target: RpcClient, invoker: RpcInvoker,
               service: RpcServiceInfo):
    if target.service and service:
        raise RuntimeError('已绑定serivce，不允许再传入新的service')

    if target.service:
        invoker.method = method
        # 当前rpc对象已绑定service
        return _do_request(invoker, target.service, 'execute')

    invoker.method = method
    return _do_request(invoker, service, 'execute')


def _do_request(invoker: AbstractInvoker, service: RpcServiceInfo, method: str):  # noqa E501
    retry = invoker.retry if hasattr(invoker, 'retry') else 0
    lb = lb_factory.create(retry, service)
    context = lb.create_context(invoker, service)
    ep_request = _request_creator(context)

    result = lb.request(method, ep_request)
    return result


rpc = RpcClient()
