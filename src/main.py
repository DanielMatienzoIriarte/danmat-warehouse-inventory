from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from rotoger import Rotoger

from src.core.inventory_redis import get_redis
from src.core.database import sessionmanager as db_sessionmanager
from src.core.config import settings as global_settings
from src.routers.product import router

#logger = Rotoger().get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.redis = await get_redis()
    #postgres_dsn = global_settings.postgres_url

    try:
        """
        await logger.ainfo(
            "Postgresql pool created",
            idle_size=app.postgres_pool.get_idle_size()
        ) """
        yield
        if db_sessionmanager._engine is not None:
            await db_sessionmanager.close()
    except Exception as exception:
        #await logger.aerror("Error during app startup", error=repr(exception))
        raise
    finally:
        await app.redis.close()
        await app.postgres_pool.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Danmat Inventory",
        version="0.0.1",
        lifespan=lifespan,
    )

    @app.get("/index")
    def get_index(request: Request):
        return {"hola": "mundo"}
    
    app.include_router(router)

    return app


app = create_app()