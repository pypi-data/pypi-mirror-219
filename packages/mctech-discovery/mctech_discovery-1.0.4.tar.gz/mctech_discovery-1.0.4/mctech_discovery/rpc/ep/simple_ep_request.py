from __future__ import absolute_import
from .ep_request import EndPointRequest
from ..request_context import EndPoint
from .internal_rpc import execute as rpc_execute, \
    stream as rpc_stream, ws as rpc_ws


class SimpleEndPointRequest (EndPointRequest):
    def execute(self, ep: EndPoint):
        resultData = rpc_execute(self.context, ep)
        return resultData

    def stream(self, ep: EndPoint):
        '''
        :return Stream
        '''
        resultStream = rpc_stream(self.context, ep)
        return resultStream

    def ws(self, ep: EndPoint):
        '''
        :return Stream
        '''
        conn = rpc_ws(self.context, ep)
        return conn
