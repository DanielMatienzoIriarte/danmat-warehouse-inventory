from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from rotoger import Rotoger

from src.core.inventory_redis import get_redis
from src.routers.product import router
from src.core.database import DatabaseSessionManager

logger = Rotoger().get_logger()
database = DatabaseSessionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    app.redis = await get_redis()

    try:
        # Attach the DB pool to the app state
        app.state.postgres_pool = database.create_db_pool()

        yield
        if database.get_db_pool():
            await database.close()

        await app.redis.close()
    except Exception as exception:
        await logger.error("Error during app startup", error=repr(exception))
        raise

app: FastAPI = FastAPI(
        lifespan=lifespan,
        title="DanMat Inventory",
        version="0.0.1"
    )

app.include_router(router)

@app.get("/health")
def get_index(request: Request):
    return {"hola": "mundo"}