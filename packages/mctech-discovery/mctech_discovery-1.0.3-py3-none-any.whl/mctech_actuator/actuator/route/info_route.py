from fastapi.responses import JSONResponse


def create_info_route(configure):
    async def info():
        return JSONResponse({
            'app': configure.get_app_info()
        })

    return info
