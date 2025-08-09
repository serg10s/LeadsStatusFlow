from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from db.database import  Base, engine
import uvicorn

from pages.rooters import root_router


app = FastAPI()
app.mount("/assets", StaticFiles(directory='assets'), name='assets')
app.include_router(root_router)

# for clear db and create new
@app.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
