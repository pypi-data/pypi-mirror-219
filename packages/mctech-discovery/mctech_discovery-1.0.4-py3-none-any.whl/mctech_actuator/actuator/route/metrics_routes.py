from ...health import manager

METRICS_PATH = '/metrics'


def create_metrics_routes(configure):
    async def metrics():
        routers = {}
        for m in manager.get_metrics():
            routers[METRICS_PATH + m['path']] = m['endpoint']
        return routers
    return metrics
