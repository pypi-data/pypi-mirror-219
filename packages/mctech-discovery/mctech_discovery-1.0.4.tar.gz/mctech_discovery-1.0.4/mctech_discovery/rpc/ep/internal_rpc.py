from __future__ import absolute_import
import requests
import asyncio

from ..web_error import WebError
from ..request_context import RequestContext, EndPoint
from ...discovery import discovery_client as client


event_loop = asyncio . get_event_loop()  # 创建一个默认的事件循环


def _create_request_option(context: RequestContext, url: str, stream: bool):
    option = {
        'method': context.invoker.method,
        'url': url,
        'data': context.invoker.body,
        'body': context.invoker.body,
        'headers': {
            'accept': 'application/json,*/*',
            'accept-encoding': 'gzip, deflate',
            'user-agent': 'nodejs rest client',
            'content-type': 'application/json',
            # 表示异步调用
            'x-client-ajax': 'true'
        }.update(context.headers),
        'timeout': 1 if not context.timeout else (context.timeout / 1000),
        'stream': stream
    }
    context.process_request_option(option)
    return option


def execute(context: RequestContext, ep: EndPoint):
    if ep:
        url = "http://%s:%d%s" % (ep.host, ep.port, context.path_and_query)
        option = _create_request_option(context, url, False)
        res: requests.Response = requests.request(
            method=option["method"],
            url=option["url"],
            data=option["body"],
            headers=option["headers"],
            timeout=option["timeout"],
            stream=option["stream"]
        )
    else:
        # 集成的是request模块
        def walk_using_urllib(url):
            option = _create_request_option(context, url, False)
            return requests.request(
                method=option["method"],
                url=option["url"],
                data=option["body"],
                headers=option["headers"],
                timeout=option["timeout"],
                stream=option["stream"]
            )

        future = client.client.walk_nodes(
            app_name=context.service.service_id,
            service=context.path_and_query,
            walker=walk_using_urllib
        )

        res: requests.Response = event_loop.run_until_complete(future)

    if res.status_code >= 400:
        timeout = context.timeout if context.timeout else -1
        service = context.service
        invoker = context.invoker

        message = "%s --> %s --> [timeout:%ds, cost: %fs] [%s] [%s] %s" % (
            res.reason, res.content, timeout, res.elapsed.total_seconds(),
            service.service_id, invoker.method, context.url)
        err = WebError(message, status=res.status_code)
        context.resolve_error(res, err)
        raise err

    content_type = res.headers['content-type'] if res.headers['content-type'] \
        else ''
    if type(content_type) == str and content_type.find('json') >= 0:
        return res.json()
    return res.text


def stream(context: RequestContext, ep: EndPoint):
    if ep:
        url = "http://%s:%d%s" % (ep.host, ep.port, context.path_and_query)
        option = _create_request_option(context, url, True)
        res: requests.Response = requests.request(
            method=option["method"],
            url=option["url"],
            data=option["body"],
            headers=option["headers"],
            timeout=option["timeout"],
            stream=option["stream"]
        )
    else:
        '''
        :return Stream
        '''
        # 集成的是request模块
        def walk_using_urllib(url):
            option = _create_request_option(context, url, True)
            return requests.request(
                method=option["method"],
                url=option["url"],
                data=option["body"],
                headers=option["headers"],
                timeout=option["timeout"],
                stream=option["stream"]
            )

        future: requests.Response = client.client.walk_nodes(
            app_name=context.service.service_id,
            service=context.path_and_query,
            walker=walk_using_urllib
        )

        res: requests.Response = event_loop.run_until_complete(future)

    if res.status_code >= 400:
        timeout = context.timeout if context.timeout else -1
        service = context.service
        invoker = context.invoker

        message = "%s --> %s --> [timeout:%ds, cost: %fs] [%s] [%s] %s" % (
            res.reason, res.content, timeout, res.elapsed.total_seconds(),
            service.service_id, invoker.method, context.url)
        err = WebError(message, status=res.status_code)
        context.resolve_error(res, err)
        raise err

    return res


def ws(context: RequestContext, ep: EndPoint):
    if ep:
        url = "ws://%s:%d%s" % (ep.host, ep.port, context.path_and_query)
    else:
        ec = client.client
        app_name = context.service.service_id.upper()
        service = context.path_and_query
        node = ec.__get_available_service(app_name)
        url = ec.__generate_service_url(node, False, False)
        if service.startswith("/"):
            url = url + service[1:]
        else:
            url = url + service

    option = _create_request_option(context, url, False)
    from websocket import create_connection
    conn = create_connection(url=option["url"],
                             timeout=option["timeout"],
                             headers=option['headers']
                             )

    return conn
