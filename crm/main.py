from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from db.database import  Base, engine

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import uvicorn

from pages.rooters import root_router


app = FastAPI()
app.mount("/assets", StaticFiles(directory='assets'), name='assets')
app.include_router(root_router)


@app.on_event('startup')
async def init_redis_cache():
    redis = aioredis.from_url("redis://127.0.0.1:6379")
    FastAPICache.init(RedisBackend(redis), prefix="email-verify")
    

@app.on_event("shutdown")
async def close_redis_connection():
    await FastAPICache.clear()  # close redis


# for clear db and create new
@app.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
