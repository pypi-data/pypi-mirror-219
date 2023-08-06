
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from .route.info_route import create_info_route
from .route.health_route import create_health_route
from .route.metrics_routes import create_metrics_routers


def create_actuator_route(configure, app: FastAPI):
    async def empty():
        res = PlainTextResponse('Actuator Not Found')
        res.status_code = 404
        return res

    management = configure.get_config('management')
    prefix = management.get('context-path') or \
        management.get('contextPath') or '/actuator'

    app.add_api_route(f"{prefix}/info", endpoint=create_info_route(configure))
    app.add_api_route(f"{prefix}/health",
                      endpoint=create_health_route(configure))
    app.add_api_route(f"{prefix}/env", endpoint=empty)
    app.add_api_route(f"{prefix}/shutdown", endpoint=empty)

    app.add_api_route(f"{prefix}/loggers", endpoint=empty)
    app.add_api_route(f"{prefix}/loggers", endpoint=empty)
    app.add_api_route(f"{prefix}/loggers/:category", endpoint=empty)

    for path, endpoint in create_metrics_routers():
        app.add_api_route(f"{prefix}/{path}", endpoint=endpoint)
