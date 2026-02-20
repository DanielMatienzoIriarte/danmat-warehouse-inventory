from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from rotoger import Rotoger

from src.core.inventory_redis import get_redis
from src.core.config import settings as global_settings
from src.routers.product import router
from src.core.database import DatabaseSessionManager

app: FastAPI = FastAPI(
        title="DanMat Inventory",
        version="0.0.1"
    )

@asynccontextmanager
async def lifespan():
    logger = Rotoger().get_logger()
    app.redis = await get_redis()
    database = DatabaseSessionManager()

    try:
        # Attach the DB pool to the app state
        app.state.postgres_pool = database.create_db_pool()

        app.include_router(router)
        yield
        if database._engine:
            await database._engine.dispose()
    except Exception as exception:
        await logger.error("Error during app startup", error=repr(exception))
        raise
    finally:
        await app.redis.close()
        await database.close()

@app.get("/health")
def get_index(request: Request):
    return {"hola": "mundo"}