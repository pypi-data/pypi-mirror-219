
from fastapi.responses import JSONResponse

from ...health import manager


def create_health_route(configure):
    async def health():
        try:
            health = manager.getHealth()
            result = health.toJson()
        except Exception as e:
            result = {
                'status': 'DOWN',
                'error': e.__str__()
            }
        return JSONResponse(result)
    return health
