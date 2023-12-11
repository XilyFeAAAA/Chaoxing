import uvicorn
import fastapi
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
# local
from app.api import api_router
from app.core.config import settings
from app.core.middleware import middlewares
from app.core.exception import exception_handlers
from app.extension.redis import cli as redisCli


@asynccontextmanager
async def app_lifespan(app: fastapi.FastAPI):
    redisCli.init_redis_connect()
    yield
    await redisCli.close_redis_connect()


app = fastapi.FastAPI(
    title=settings.SERVER_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    middleware=middlewares,
    exception_handlers=exception_handlers,
    lifespan=app_lifespan
)


app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_KEY, same_site="none", https_only=True)
app.include_router(api_router, prefix=settings.API_V1_STR, tags=settings.API_V1_TAG)

# Start uvicorn server
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.HOST,
        port=settings.PORT,
        server_header=False,
    )
