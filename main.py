from fastapi import FastAPI

from routes.price_routes import router as price_router

app = FastAPI()

app.include_router(price_router)


@app.get("/", response_model=dict)
async def root() -> dict:
    return {"Message": "Hello world!"}


@app.post("/")
async def recreate_tables():
    from core.setup import Base, async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"Message": "All tables were recreated"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
