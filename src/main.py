import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.config import settings

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager

from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(1)
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()
    print(2)

# if settings.MODE == 'TEST':
#     FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_auth)
app.include_router(router=router_hotels)
app.include_router(router=router_rooms)
app.include_router(router=router_bookings)
app.include_router(router=router_facilities)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
