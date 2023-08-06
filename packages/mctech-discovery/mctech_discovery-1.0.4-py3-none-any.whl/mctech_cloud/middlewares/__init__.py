from .service_context_middleware import ServiceContextMiddleware
from log4py import logging
from fastapi import FastAPI
from mctech_actuator import create_actuator_route

log = logging.getLogger('python.cloud.middlewares')


def create_extras(converters, app: FastAPI):
    """创建构建extras的middleware
    """
    app.add_middleware(ServiceContextMiddleware, converters=converters)
    log.info('创建extras context middleware完成')


def create_actuator(configure, app: FastAPI):
    """创建用于Actuator服务治理相关api的router
    """

    # 设置actuator的router
    create_actuator_route(configure, app)
    log.info('创建actuator router完成')
