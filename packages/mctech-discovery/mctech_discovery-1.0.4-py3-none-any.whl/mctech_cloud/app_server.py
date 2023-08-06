import uvicorn
import math

from log4py import logging
from fastapi import FastAPI
from mctech_discovery.discovery import discovery_client, configure
from . import middlewares

log = logging.getLogger('python.cloud.appServer')


def try_convert_number(val: str):
    ret = int(val)
    return val if math.isnan(ret)else ret


def init_app_manager():
    # log.info('开始初始化各部分组件......')
    # #  配置合并完成，开始触发执行延迟初始化事件
    # #  @ts-expect-error 未暴露方法
    # appManager.onIniting(configure)
    # log.info('组件初始化完成！')
    pass


class AppServer:
    def __init__(self):
        self._app = FastAPI()
        self._converters = {
            'x-tenant-id': try_convert_number,
            'x-user-id': try_convert_number,
            'x-id': try_convert_number,
            'x-org-id': try_convert_number
        }

    @property
    def app(self):
        return self._app

    def _init(self):
        middlewares.create_actuator(configure, self._app)
        init_app_manager()
        middlewares.create_extras(self._converters, self._app)

    def start(self):
        # 启动eureka(当前应用不会注册到注册中心)
        discovery_client.start()
        #  通过注册中心找到配置服务，加载远程配置
        discovery_client.load_config()
        configure.merge()
        #  初始化本地模块
        self._init()
        #  根据需要把当前应用注册到服务中心
        discovery_client.register()

        #  启动网站
        info = configure.get_app_info()
        port = info['port']

        #  添加'0.0.0.0'的目的是要求ctx.ip返回的格式是ipv4
        uvicorn.run(self._app, host="0.0.0.0", port=port, access_log=False)
        if log.isInfoEnabled():
            log.info("应用程序在端口 %s 启动完成." % port)

    def stop(self):
        discovery_client.unregister()
